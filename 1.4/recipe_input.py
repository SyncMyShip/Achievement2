import pickle


# Determine difficulty of the recipe
def calc_difficulty():
    for recipe in recipes_list:
        difficulty = "Easy" if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4 \
            else "Medium" if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4 \
            else "Intermediate" if recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4 \
            else "Hard" 
        
        return difficulty

# Create recipe dict from user input
def take_recipe():
    name = input("Recipe name: ")
    cooking_time = int(input("Estimated cook time: "))
    ingredients = str(input("Ingredients: ")).split()

    difficulty = calc_difficulty()

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

    return recipe
    

# Allow user to enter filename to stored recipes
filename = input("Enter the name of the file where your recipes are stored: ")

# Try opening user file, generate new file if not found
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        print("File successfully loaded!")
except FileNotFoundError:
    print("File not found - new file created")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
except:
    print("File not found - new file created")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    file.close()
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]
    

# Allow user to define a number of recipes to enter
n = int(input("How many recipes would you like to enter? "))


for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)
    print("Recipe successfully added!")

    
# Create new, updated dictionary    
data = {
    "recipe_list": recipes_list,
    "all_ingredients": all_ingredients
}    


# Opens and save data to the file
updated_file = open(filename, "wb")
pickle.dump(data, updated_file)
updated_file.close()
print("Recipe file successfully updated!")