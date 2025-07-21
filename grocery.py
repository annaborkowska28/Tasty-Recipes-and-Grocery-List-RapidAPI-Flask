from flask import Blueprint, render_template, request, redirect, url_for, flash
from collections import Counter
from unit_conversions import convert_to_grams
from fractions import Fraction
import re

grocery_bp = Blueprint('grocery', __name__)
grocery_counter = Counter()


unicode_fractions = {
    '¼': '1/4', '½': '1/2', '¾': '3/4',
    '⅐': '1/7', '⅑': '1/9', '⅒': '1/10',
    '⅓': '1/3', '⅔': '2/3',
    '⅕': '1/5', '⅖': '2/5', '⅗': '3/5', '⅘': '4/5',
    '⅙': '1/6', '⅚': '5/6',
    '⅛': '1/8', '⅜': '3/8', '⅝': '5/8', '⅞': '7/8'
}


# extract quantity, unit and name
def extract_quantity_and_unit(ingredient):
    ingredient = ingredient.strip()

    # Sprawdzenie składników opcjonalnych
    if any(phrase in ingredient.lower() for phrase in ["to taste", "a pinch", "as needed", "optional", "for garnish"]):
        return ingredient, None, ""

    match = re.match(r"^\s*(\d+\s\d+/\d+|\d+/\d+|\d+|[" + "".join(unicode_fractions.keys()) + r"])?\s*(.*)", ingredient)

    if match:
        raw_qty = match.group(1)
        name = match.group(2).strip()

        try:
            if raw_qty:
                if raw_qty in unicode_fractions:
                    raw_qty = unicode_fractions[raw_qty]
                if ' ' in raw_qty:  # np. '1 1/2'
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


# Add ingredients from recipe
@grocery_bp.route('/add-to-grocery-list/<int:recipe_id>', methods=['POST'])
def add_to_grocery_list(recipe_id):
    from main import recipes  # import here to avoid circular imports
    requested_recipe = next((rec for rec in recipes if rec['id'] == recipe_id), None)
    if requested_recipe:
        for raw_ingredient in requested_recipe['ingredients']:
            raw_text = raw_ingredient.strip().lower()
            if any(phrase in raw_text for phrase in ["to taste", "a pinch", "as needed", "optional", "for garnish"]):
                grocery_counter[(raw_ingredient.strip(), None)] = None
                continue
            ingredient_name, quantity, unit = extract_quantity_and_unit(raw_ingredient)
            for suffix in [", chopped", ", diced", ", shredded", ", cooked", ", minced", ", sliced"]:
                if ingredient_name.lower().endswith(suffix):
                    ingredient_name = ingredient_name[: -len(suffix)].strip()
            grams = convert_to_grams(ingredient_name, quantity, unit) if quantity is not None else None
            if grams:
                grocery_counter[(ingredient_name, 'g')] += grams
            elif quantity is not None:
                grocery_counter[(ingredient_name, unit)] += quantity
            else:
                grocery_counter[(ingredient_name, None)] = None
    return redirect(url_for('grocery.view_grocery_list', recipe_id=recipe_id))

# Display grocery list
@grocery_bp.route('/view-grocery-list', methods=['GET'])
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

# Remove single item
@grocery_bp.route('/remove-from-grocery-list', methods=['POST'])
def remove_from_grocery_list():
    ingredient_name = request.form.get('ingredient', '').strip()
    unit = request.form.get('unit', '').strip()
    key = (ingredient_name, unit)
    print(grocery_counter)
    if key in grocery_counter:
        del grocery_counter[key]
        flash(f'Removed "{ingredient_name}" from the list.', "info")
    else:
        flash("Could not find that ingredient in the list.", "warning")
    return redirect(url_for('grocery.view_grocery_list'))

#  Clear list
@grocery_bp.route('/clear-grocery-list', methods=['POST'])
def clear_grocery_list():
    grocery_counter.clear()
    flash("All items removed from the grocery list.", "info")
    return redirect(url_for('grocery.view_grocery_list'))