
import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv



app = Flask(__name__)
Bootstrap5(app)
url = "https://tasty.p.rapidapi.com/recipes/list"

querystring = {"from": "0", "size": "20", "tags": "under_30_minutes"}



load_dotenv()
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
	return render_template('index.html', all_recipes=recipes)


@app.route('/rec/<int:index>')
def single_recipe(index):
	requested_recipe = None
	for recipe_id in recipes:
		if recipe_id['id'] == index:
			requested_recipe = recipe_id
	return render_template('single.html', recipe=requested_recipe)



@app.route('/contact')
def contact():
	return render_template("contact.html")


@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)
