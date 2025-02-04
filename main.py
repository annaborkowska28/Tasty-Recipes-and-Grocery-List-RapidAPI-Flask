import datetime
import re
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import smtplib


load_dotenv()
app = Flask(__name__)
Bootstrap5(app)
url = "https://tasty.p.rapidapi.com/recipes/list"

querystring = {"from": "0", "size": "20", "tags": "under_30_minutes"}

my_email = os.getenv('email')
password = os.getenv('password')
headers = {
    "x-rapidapi-key": os.getenv('KEY'),
    "x-rapidapi-host": "tasty.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()
    recipes = data.get('results', [])

    for recipe in recipes:
        ingredients = recipe['sections'][0]['components']
        ingredient_list = [ingredient['raw_text'] for ingredient in ingredients]
        recipe['ingredients'] = ingredient_list

else:
    print("Failed to retrieve data. Status code:", response.status_code)


@app.route('/')
def home():
    # for dynamic footer
    current_year = datetime.now().year
    return render_template('index.html', all_recipes=recipes, current_year=current_year)


@app.route('/rec/<int:index>')
def single_recipe(index):
    requested_recipe = None
    for recipe_id in recipes:
        if recipe_id['id'] == index:
            requested_recipe = recipe_id
    return render_template('single.html', recipe=requested_recipe)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        contact_data = request.form
        send_email(contact_data["name"], contact_data["email"], contact_data["phone"], contact_data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

GMAIL_SMTP_SERVER = "smtp.gmail.com"
PORT = 587

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\n{message}\n Name: {name}\nEmail: {email}\nPhone: {phone}\n"
    with smtplib.SMTP(GMAIL_SMTP_SERVER, port=587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(from_addr=GMAIL_SMTP_SERVER, to_addrs=my_email, msg=email_message)


@app.route('/about')
def about():
    return render_template('about.html')


my_grocery_list = {}

def extract_quantity_and_unit(ingredient):
    match = re.match(r"(\d+)\s*(\w*)\s(.*)", ingredient)
    if match:
        quantity = int(match.group(1))
        unit = match.group(2)
        ingredient_name = match.group(3)
    else:
        quantity = 1
        unit = ''
        ingredient_name = ingredient
    return ingredient_name, quantity, unit



@app.route('/add-to-grocery-list/<int:recipe_id>', methods=['POST'])
def add_to_grocery_list(recipe_id):
    """adding ingredients from a recipe to the grocery list while
    summing the quantities if the same ingredient is already present in the list."""
    def add_ingredient_to_list(ingredient_name, quantity, unit, recipe_id):
        ingredient_found = False
        for item in my_grocery_list.values():
            existing_item = next((x for x in item if x['ingredient'] == ingredient_name and x['unit'] == unit), None)
            if existing_item:
                existing_item['quantity'] += quantity
                ingredient_found = True
                break
        if not ingredient_found:
            if recipe_id not in my_grocery_list:
                my_grocery_list[recipe_id] = []
            my_grocery_list[recipe_id].append({'ingredient': ingredient_name, 'unit': unit, 'quantity': quantity})

    # Find the requested recipe
    requested_recipe = next((rec for rec in recipes if rec['id'] == recipe_id), None)
    if requested_recipe:
        # If the recipe is found, loop through its ingredients
        for ingredient in requested_recipe['ingredients']:
            ingredient_name, quantity, unit = extract_quantity_and_unit(ingredient)
            add_ingredient_to_list(ingredient_name, quantity, unit, recipe_id)
        return redirect(url_for('view_grocery_list'))


@app.route('/view-grocery-list', methods=['GET'])
def view_grocery_list():
    # Loop through all items in the grocery list
    full_grocery_list = []
    def add_to_full_list(item):
        existing_item = next(
            (x for x in full_grocery_list if x['ingredient'] == item['ingredient'] and x['unit'] == item['unit']), None)
        if existing_item:
            existing_item['quantity'] += item['quantity']
        else:
            full_grocery_list.append(item)

    for items in my_grocery_list.values():
        for item in items:
            add_to_full_list(item)
    return render_template('groceries.html', grocery_list=full_grocery_list)


if __name__ == '__main__':
    app.run(debug=True)
