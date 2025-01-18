from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String

import pymysql
pymysql.install_as_MySQLdb()


# Connect to task_database
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Setup session object for db manipulation
Session = sessionmaker(bind=engine)
session = Session()

# Define SQLAlchemy declarative base class
Base = declarative_base()

# Define Recipe class
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"
    
    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"{'-'*40}\n"
            f"Recipe ID:  {self.id}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time}\n"
            f"Difficulty: {self.difficulty}\n"
        )
    

    # Calculate difficulty based on cooking_time and number of ingredients
    def calc_difficulty(self):
        print("\nUpdating difficulty...")

        difficulty = "Easy" if self.cooking_time < 10 and len(self.ingredients) < 4 \
            else "Medium" if self.cooking_time < 10 and len(self.ingredients) >= 4 \
            else "Intermediate" if self.cooking_time >= 10 and len(self.ingredients) < 4 \
            else "Hard" if self.cooking_time >= 10 and len(self.ingredients) >= 4 \
            else print("Unable to calculate difficulty, please try again")

        self.difficulty = difficulty


    def return_ingredients_as_list(self):
        if self.ingredients:
            return self.ingredients.split(", ")
        else:
            return []
        

# Create database table
Base.metadata.create_all(engine)


##### Main Operations #####

# Function 1: create_recipe()
def create_recipe():
    # Enter recipe name & check if alphanumeric and <= 50 char
    name = input("\nEnter recipe name: ")

    # Requirements = 50 or less char, alphanumeric, allow spaces
    if len(name) > 50 or not all(char.isalnum() or char.isspace() for char in name): 
        print("Name is invalid - no more than 50 characters allowed")
        return
    
    ingredients = []
    ingredient_num = int(input("How many ingredients are in your recipe? "))
    for i in range(ingredient_num):
        ingredient = input("Enter ingredient: ")
        ingredients.append(ingredient)
    ingredients_string = ", ".join(ingredients)

    # Enter cook time & check that input is int
    cooking_time = int(input("Enter cooking time (minutes): "))
    # if not cooking_time.isnumeric():
    #     print("Cooking time is invalid - only numbers allowed")
    #     return
    
    # use recipe details to calculate difficulty
    recipe_entry = Recipe(
        name=name, 
        ingredients=ingredients_string,
        cooking_time=int(cooking_time)
    )

    recipe_entry.calc_difficulty()

    # Add recipe to session
    session.add(recipe_entry)
    session.commit()
    print("Recipe successfully added!")


# Function 2: view_all_recipes()
def view_all_recipes():
    recipes = session.query(Recipe).all()

    if len(recipes) == 0:
        print("No recipes found")
        return
    else:
        print("\n Full List of Recipes: ")
        print("-" * 30)

        for recipe in recipes:
            print(recipe)


# Function 3: search_by_ingredients()
def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("No recipes found")
        return
    
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []

    for result in results:
        tmp_ingredient_list = result[0].split(", ")
        for ingredient in tmp_ingredient_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)


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

        print("\nYou selected the ingredient: ", ingredient_searched + "\n")

        conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in ingredient_searched]

        recipes = session.query(Recipe).filter(*conditions).all()

    except:
        print("An unexpected error occurred. Make sure to select a valid number from the list.")

    else:
        for recipe in recipes:
            print(recipe)


# Function 4: edit_recipe()
def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes found")
        return
    else:
        results = session.query(Recipe.id, Recipe.name).all()
        for recipe_id, name in results:
            print(f"{recipe_id}: {name}")

    selected_recipe_id = (input("\nEnter recipe ID to edit: "))
    if not selected_recipe_id.isnumeric():
        print("Please select a valid ID")
        return
    
    recipe_to_edit = session.query(Recipe).filter_by(id=int(selected_recipe_id)).first()

    if not recipe_to_edit:
        print("No recipes found")
        return
    
    print(f"\nRecipe Details: ")
    print("-" * 30)
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time}")

    attribute_to_edit = input("\nEnter the number corresponding to the attribute you'd like to edit: ")
    if attribute_to_edit not in ["1", "2", "3"]:
        print("Invalid selection - please select an attribute number")
        return
    
    # Logic to update recipe name
    if attribute_to_edit == "1":
        updated_name = input("\nEnter the new recipe name: ")
        if len(updated_name) > 50:
            print("Too many characters! - No more than 50 characters allowed")
            return
        elif not all(char.isalnum() or char.isspace() for char in updated_name):
            print("Invalid character(s) - Only alphanumeric characters allowed")
            return
        recipe_to_edit.name = updated_name

    # Logic to update recipe ingredient(s)
    elif attribute_to_edit == "2":
        new_ingredients = []
        ingredient_num = int(input("\nHow many ingredients would you like to add? "))

        for i in range(ingredient_num):
            ingredient = input("Enter an ingredient: ")
            new_ingredients.append(ingredient)
        recipe_to_edit.ingredients = ", ".join(new_ingredients)
    
    # Logic to update cooking time
    elif attribute_to_edit == "3":
        new_cook_time = input("\nEnter the new cooking time (min): ")
        if not new_cook_time.isnumeric():
            print("Invalid cooking time - Only numbers allowed")
            return
        recipe_to_edit.cooking_time = int(new_cook_time)

    # Recalculate difficulty
    recipe_to_edit.calc_difficulty()
    session.commit()
    print("\nRecipe updated successfully!")


# Function 5: delete_recipe()
def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes found")
        return
    
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, name in results:
        print(f"{recipe_id}: {name}")

    selected_recipe = input("\nEnter the ID of the recipe you'd like to delete: ")
    if not selected_recipe.isnumeric():
        print("ID is not valid")
        return
    
    recipe_to_delete = session.query(Recipe).filter_by(id=int(selected_recipe)).first()
    if not recipe_to_delete:
        print("Recipe not found")
        return
    
    confirm_deletion = input(f"\nAre you sure you want to delete {recipe_to_delete.name}? (y/n):" )

    if (confirm_deletion.lower() == "y", "yes"):
        session.delete(recipe_to_delete)
        session.commit()
        print("\nRecipe deleted successfully")
    else:
        print("\nOperation has been cancelled")
        return


# Main Menu
def main_menu():
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
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        elif choice == "quit":
            print("Exiting...")
            # close session
            session.close()
            # displose of existing connection pool
            engine.dispose()
            break
        else: 
            print("\nInvalid selection - please select a valid option")


# Start the main menu
main_menu()
