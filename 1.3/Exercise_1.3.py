recipes_list = []
ingredients_list = []


def take_recipe():
    name = input("Recipe name: ")
    cooking_time = int(input("Estimated cook time: "))
    ingredients = str(input("Ingredients: ")).split()

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }

    return recipe


n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)


for recipe in recipes_list:
    difficulty = "Easy" if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4 \
        else "Medium" if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4 \
        else "Intermediate" if recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4 \
        else "Hard" 
    
    recipe_ingredients = recipe["ingredients"] 
    
    # Print recipe details
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe_ingredients:
        print(f"{ingredient}")
    print(f"Difficulty: {difficulty}")

# Print ingredients
sorted_ingredients = sorted(ingredients_list)
print("\nAll Ingredients Across All Recipes:")
print('─' * 50)
for i in sorted_ingredients:
    print(f"{i}")