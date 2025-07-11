import requests
from datetime import datetime
from flask import Flask, render_template, request, abort
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import smtplib
from templates.grocery import grocery_bp



app = Flask(__name__)
app.register_blueprint(grocery_bp)
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