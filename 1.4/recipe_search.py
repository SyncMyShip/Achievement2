import pickle


def display_recipe(recipe):
    # Print recipe details
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"{"- ", ingredient}")
    print(f"Difficulty: {recipe['difficulty']}")


def search_ingredients(data):
    available_ingredients = enumerate(data["all_ingredients"])
    enumerated_list = list(available_ingredients)

    for i in enumerated_list:
        index = i[0]
        ingredient = i[1]
        print(index, ingredient)

    try:
        num = int(input("Pick an ingredient by number: "))
        ingredient_searched = enumerated_list[num][1]
        print("Searching...")
    except ValueError:
        print("Only numbers are allowed")
    except:
        print("No ingredients found - please enter a number from the list of available ingredients")
    else:
        for i in data["recipe_list"]:
            if ingredient_searched in i["ingredients"]:
                # Print recipe details
                print(f"\nRecipe: {i['name']}")
                print(f"Cooking Time (min): {i['cooking_time']}")
                print("Ingredients:")
                for ingredient in i["ingredients"]:
                    print(f"- {ingredient}")
                print(f"Difficulty: {i['difficulty']}")


# Allow user to enter filename to store recipes
filename = input("Enter the name of file where recipes should be stored: ")

# Try opening user file, generate new file if not found
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        print("File successfully loaded!")
except FileNotFoundError:
    print("File not found - new file created")
except:
    print("Unexpected error encountered - please try again later")
else:
    file.close()
    search_ingredients(data)