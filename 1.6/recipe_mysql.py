# import mysql.connector
import pymysql

# Establish connection to the MySQL database
conn = pymysql.connect(
    host="localhost",
    user="cf-python",
    passwd="password"
)

# Initialize cursor object
cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Switch to the created database
cursor.execute("USE task_database")

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)      
)''')


def calc_difficulty(cooking_time, ingredients):
    print("Updating difficulty...")

    difficulty = "Easy" if cooking_time < 10 and len(ingredients) < 4 \
        else "Medium" if cooking_time < 10 and len(ingredients) >= 4 \
        else "Intermediate" if cooking_time >= 10 and len(ingredients) < 4 \
        else "Hard" if cooking_time >= 10 and len(ingredients) >= 4 \
        else print("Unable to calculate difficulty, please try again")

    print("Difficulty: ", difficulty)
    return difficulty


def create_recipe(conn, cursor):
    ingredients = []
    name = input("\nEnter recipe name: ")
    cooking_time = int(input("Enter cooking time (minutes): "))
    ingredient = input("Enter recipe ingredients: ")
    ingredients.append(ingredient)
    difficulty = calc_difficulty(cooking_time, ingredients)
    ingredients_string = ", ".join(ingredients)
    
    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, ingredients_string, cooking_time, difficulty)
    
    cursor.execute(sql, val)
    conn.commit()
    print("Recipe saved.")


def search_recipe(conn, cursor):
    all_ingredients = []
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    # Loop through each recipe to extract ingredients
    for recipe_ingredients_list in results:
        for recipe_ingredients in recipe_ingredients_list:
            # Assuming ingredients are comma-separated in the database
            recipe_ingredient_split = recipe_ingredients.split(", ")

            # Add each ingredient as a separate item in the all_ingredients list
            all_ingredients.extend(recipe_ingredient_split)

    # Remove duplicate ingredients
    all_ingredients = list(dict.fromkeys(all_ingredients))

    print("\nAll ingredients list:")
    print("-" * 25)

    # Now enumerate over each unique ingredient
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}. {ingredient}")

    try:
        ingredient_searched_number = input(
            "\nEnter the number corresponding to the ingredient you want to select from the above list: ")

        ingredient_searched_index = int(ingredient_searched_number) - 1

        ingredient_searched = all_ingredients[ingredient_searched_index]

        print("\nYou selected the ingredient: ", ingredient_searched)

    except ValueError:
        print("An unexpected error occurred. Make sure to select a valid number from the list.")

    else:
        print("\nThe recipe(s) below include the selected ingredient: ")
        print("-------------------------------------------------------")

        cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ('%' + ingredient_searched + '%'))
        result_recipe = cursor.fetchall()

        for row in result_recipe:
            print("\nID: ", row[0])
            print("Name: ", row[1])
            print("Ingredients: ", row[2])
            print("Cooking Time: ", row[3])
            print("Difficulty: ", row[4])


def update_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id = int((input("\nEnter recipe ID to update: ")))
    update_column = str(input("\nEnter a field to update (name, cooking_time, ingredients): "))
    update_value = (input("\nEnter your new recipe details: "))
    print(f"Your selection: {update_value}")

    if update_column == "name":
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (update_value, recipe_id))
        print("Name updated successfully!")
        print(f"Updated Name: {update_value}")

    elif update_column == "cooking_time":
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (update_value, recipe_id))
        # cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe = cursor.fetchall()

        name = result_recipe_for_update[0][1]
        recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
        cooking_time = result_recipe_for_update[0][3]

        updated_difficulty = calc_difficulty(int(update_value), recipe_ingredients)
        print("Updated difficulty: ", updated_difficulty)

        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, recipe_id))
        print("Difficulty successfully updated!")

    elif update_column == "ingredients":
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (update_value, recipe_id))
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        result_recipe_for_update = cursor.fetchall()

        print("result_recipe_for_update: ", result_recipe_for_update)

        name = result_recipe_for_update[0][1]
        recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
        cooking_time = result_recipe_for_update[0][3]
        # difficulty = result_recipe_for_update[0][4]

        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        print("Updated difficulty: ", updated_difficulty)

        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, recipe_id))
        print("Difficulty successfully updated!")

    conn.commit()


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    removed_recipe = (input("\nEnter the recipe ID to delete: "))
    cursor.execute("DELETE FROM Recipes WHERE id = (%s)", (removed_recipe, ))

    conn.commit()
    print("\nRecipe deleted successfully.")


def view_all_recipes(conn, cursor):
    print("\nAll recipes can be found below: ")
    print('─' * 30)

    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    for row in results:
        print("\nID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty: ", row[4])


def main_menu(conn, cursor):
    choice = ""
    while (choice != "quit"):
        print("\n======================================================")
        print("\nMain Menu:")
        print("-------------")
        print("Pick a choice:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Update an existing recipe")
        print("   4. Delete a recipe")
        print("   5. View all recipes")
        print("\n   Type 'quit' to exit the program.")
        choice = input("\nYour choice: ")
        print("\n======================================================\n")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            view_all_recipes(conn, cursor)


main_menu(conn, cursor)
print("Exiting...")
conn.close()