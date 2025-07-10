
conversion_table = {
    ('milk', 'cup'): 240,
    ('olive oil', 'tablespoon'): 13,
    ('lime juice', 'tablespoon'): 13,
    ('plain greek yogurt', 'cup'): 245,
    ('chicken breasts', 'piece'): 174,
    ('chicken', 'cup'): 140,
    ('sugar', 'cup'): 200,
    ('flour', 'cup'): 120,
    ('avocado', 'piece'): 200,
    ('egg', 'piece'): 50
}



def convert_to_grams(ingredient_name, quantity, unit):
    name = ingredient_name.lower().strip()
    unit = unit.lower().strip()

    unit_aliases = {
        'tablespoons': 'tablespoon',
        'tbsp': 'tablespoon',
        'tbs': 'tablespoon',
        'teaspoons': 'teaspoon',
        'tsp': 'teaspoon',
        'cups': 'cup',
        'pieces': 'piece',
        'pcs': 'piece'
    }
    unit = unit_aliases.get(unit, unit)

    key = (name, unit)
    if key in conversion_table:
        grams = quantity * conversion_table[key]
        return round(grams)
    return None