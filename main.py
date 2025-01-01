import requests
from flask import Flask, render_template


app = Flask(__name__)
url = "https://tasty.p.rapidapi.com/recipes/list"

querystring = {"from": "0", "size": "20", "tags": "under_30_minutes"}

headers = {
	"x-rapidapi-key": "db8c349c0bmsh53af7fa3ab0b86bp1455e3jsnae05c5c7d1f5",
	"x-rapidapi-host": "tasty.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
	data = response.json()
	recipes = data.get('results', [])

	for recipe in recipes:
		recipe_id = recipe['id']
		image_url = recipe['thumbnail_url']
		recipe_name = recipe['name']

		description = recipe['description']

		ingredients = recipe['sections'][0]['components']
		ingredient_list = [ingredient['raw_text'] for ingredient in ingredients]
		instructions = recipe['instructions']
		instruction_list = [instruction['display_text'] for instruction in instructions]


else:
	print("Failed to retrieve data. Status code:", response.status_code)


@app.route('/')
def home():
	return render_template('index.html', all_recipes=recipes)


@app.route('/rec/<int:index>')
def single_recipe(index):
	requested_recipe = None
	for rec in recipes:
		if rec['id'] == index:
			requested_recipe = rec
	return render_template('single.html', recipe=requested_recipe, ingredient_list=ingredient_list, instruction_list=instruction_list, image_url=image_url)






if __name__ == '__main__':
	app.run(debug=True)