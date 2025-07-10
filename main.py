import re
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import smtplib
from collections import Counter
from fractions import Fraction

from unit_conversions import convert_to_grams

app = Flask(__name__)
Bootstrap5(app)


load_dotenv()
app.secret_key = os.getenv('secret_k')


url = "https://tasty.p.rapidapi.com/recipes/list"
querystring = {"from": "0", "size": "20", "tags": "under_30_minutes"}
headers = {
    "x-rapidapi-key": os.getenv('KEY'),
    "x-rapidapi-host": "tasty.p.rapidapi.com"
}


my_email = os.getenv('email')
password = os.getenv('password')
GMAIL_SMTP_SERVER = "smtp.gmail.com"
PORT = 587

# Grocery List Stoage
grocery_counter = Counter()


def fetch_recipes():
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        for recipe in data.get('results', []):
            recipe['ingredients'] = [ingredient['raw_text'] for ingredient in recipe['sections'][0]['components']]
        return data.get('results', [])
    else:
        print("Error fetching data", response.status_code)
        return []

recipes = fetch_recipes()

# Parse quantity and ingredient name from raw text
def extract_quantity_and_unit(ingredient):
    ingredient = ingredient.strip()

    # Skip parsing for non-measurable items
    if any(phrase in ingredient.lower() for phrase in ["to taste", "a pinch", "as needed", "optional"]):
        return ingredient, None, ""

    # Match numeric quantities including fractions and unicode
    match = re.match(
        r"^\s*(\d+\s\d+/\d+|\d+/\d+|\d+|[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞])?\s*(.*)",
        ingredient.strip()
    )

    if match:
        raw_qty = match.group(1)
        name = match.group(2).strip()

        # Parse numeric quantity safely
        try:
            if raw_qty:
                if ' ' in raw_qty:
                    whole, frac = raw_qty.split()
                    quantity = int(whole) + float(Fraction(frac))
                else:
                    quantity = float(Fraction(raw_qty))
            else:
                quantity = 1
        except Exception as e:
            print(f"Parse error: {e}")
            quantity = 1
    else:
        name = ingredient.strip()
        quantity = 1

    return name, quantity, ""

@app.route('/')
def home():
    current_year = datetime.now().year
    return render_template('index.html', all_recipes=recipes, current_year=current_year)

# Single recipe display
@app.route('/rec/<int:index>')
def single_recipe(index):
    requested_recipe = next((recipe for recipe in recipes if recipe['id'] == index), None)
    if requested_recipe is None:
        abort(404)
    return render_template('single.html', recipe=requested_recipe)

# Contact form & message sending
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        contact_data = request.form
        send_email(contact_data["name"],
                   contact_data["email"],
                   contact_data["phone"],
                   contact_data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject: New Message\n\n{message}\n Name: {name}\nEmail: {email}\nPhone: {phone}\n"
    with smtplib.SMTP(GMAIL_SMTP_SERVER, port=PORT) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=email_message)


@app.route('/about')
def about():
    return render_template('about.html')

# Add ingredients from recipe to grocery list
@app.route('/add-to-grocery-list/<int:recipe_id>', methods=['POST'])
def add_to_grocery_list(recipe_id):
    requested_recipe = next((rec for rec in recipes if rec['id'] == recipe_id), None)

    if requested_recipe:
        for raw_ingredient in requested_recipe['ingredients']:
            raw_text = raw_ingredient.strip().lower()

            # Skip or add non-measurable items with no quantity
            if any(phrase in raw_text for phrase in ["to taste", "a pinch", "as needed", "optional", "for garnish"]):
                grocery_counter[(raw_ingredient.strip(), None)] = None
                continue

            # Parse and clean ingredient
            ingredient_name, quantity, unit = extract_quantity_and_unit(raw_ingredient)

            for suffix in [", chopped", ", diced", ", shredded", ", cooked", ", minced", ", sliced"]:
                if ingredient_name.lower().endswith(suffix):
                    ingredient_name = ingredient_name[: -len(suffix)].strip()

            #  Convert to grams if possible
            grams = convert_to_grams(ingredient_name, quantity, unit) if quantity is not None else None

            if grams:
                grocery_counter[(ingredient_name, 'g')] += grams
            elif quantity is not None:
                grocery_counter[(ingredient_name, unit)] += quantity
            else:
                grocery_counter[(ingredient_name, None)] = None

    return redirect(url_for('view_grocery_list', recipe_id=recipe_id))

# Display grocery list
@app.route('/view-grocery-list', methods=['GET'])
def view_grocery_list():
    recipe_id = request.args.get('recipe_id')
    full_grocery_list = []

    for (name, unit), qty in grocery_counter.items():
        if qty is None:
            full_grocery_list.append({
                'ingredient': name,
                'unit': '',
                'quantity': None
            })
        else:
            pretty_qty = int(qty) if qty == int(qty) else round(qty, 2)
            full_grocery_list.append({
                'ingredient': name,
                'unit': unit,
                'quantity': pretty_qty
            })
    return render_template('groceries.html', grocery_list=full_grocery_list, recipe_id=recipe_id)

# Remove individual item from grocery list
@app.route('/remove-from-grocery-list', methods=['POST'])
def remove_from_grocery_list():
    ingredient_name = request.form.get('ingredient', '').strip()
    unit = request.form.get('unit', '').strip()
    key = (ingredient_name, unit)

    if key in grocery_counter:
        del grocery_counter[key]
        flash(f'Removed "{ingredient_name}" from the list.', "info")
    else:
        flash("Could not find that ingredient in the list.", "warning")

    return redirect(url_for('view_grocery_list'))

#Clear entire grocery list
@app.route('/clear-grocery-list', methods=['POST'])
def clear_grocery_list():
    grocery_counter.clear()
    flash("All items removed from the grocery list.", "info")
    return redirect(url_for('view_grocery_list'))

# Search bar for recipes
@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return render_template('search_results.html', results=[], query=query)

    matching = [
        recipe for recipe in recipes
        if query in recipe['name'].lower() or any(query in ingredient.lower() for ingredient in recipe['ingredients'])
    ]

    return render_template('search_results.html', results=matching, query=query)

# 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)