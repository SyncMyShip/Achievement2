recipe_1 = {
    "name": "Tea",
    "Cooking time": 5,
    "Ingredients": [
        "Tea leaves",
        "Sugar",
        "Water"
    ]
}

recipe_2 = {
    "name": "Chocolate Chip Cookies",
    "Cooking time": 12,
    "Ingredients": [
        "Eggs",
        "Flour",
        "Butter",
        "Sugar",
        "Chocolate chips",
        "Baking soda", 
        "Salt",
        "Vanilla"
    ]
}

recipe_3 = {
    "name": "Coffee",
    "Cooking time": 5,
    "Ingredients": [
        "Coffee grounds",
        "Sugar",
        "Creamer",
    ]
}

recipe_4 = {
    "name": "French Toast",
    "Cooking time": 5,
    "Ingredients": [
        "Bread",
        "Eggs",
        "Vanilla extract",
        "Cinnamon",
        "Nutmeg"
    ]
}

recipe_5 = {
    "name": "Grilled Cheese",
    "Cooking time": 12,
    "Ingredients": [
        "Bread",
        "Cheese",
        "Garlic",
        "Butter",
        "Parsley"
    ]
}

all_recipes = [
    recipe_1,
    recipe_2,
    recipe_3,
    recipe_4,
    recipe_5
]

for recipe in all_recipes:
    print(recipe['Ingredients'])