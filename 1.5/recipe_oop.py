class Recipe(object):
    all_ingredients = {}

    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None

        self.get_difficulty()

    # Getters for name and cooking time
    def get_name(self):
        return self.name
    
    def get_cooking_time(self):
        return self.cooking_time
    
    # Setters for name and cooking time
    def set_name(self, name):
        self.name = name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time


    # def __len__(self, ingredients): 
    #     return len(ingredients)

    def add_ingredients(self, *ingredient):
        self.ingredients.extend(ingredient)
        self.update_all_ingredients()

    # Getter for ingredients
    def get_ingredients(self):
        return self.ingredients


    def calc_difficulty(self):
        difficulty = "Easy" if self.cooking_time < 10 and len(self.ingredients) < 4 \
            else "Medium" if self.cooking_time < 10 and len(self.ingredients) >= 4 \
            else "Intermediate" if self.cooking_time >= 10 and len(self.ingredients) < 4 \
            else "Hard" 
        
        self.difficulty = difficulty
        return difficulty

    # Getter for difficulty
    def get_difficulty(self):
        if self.difficulty is None:
            self.calc_difficulty()
        else:
            return self.difficulty

    def search_ingredients(self, ingredient):
        # print(f"Searching for {ingredient}")
        if ingredient in self.ingredients:
            # print(f"{ingredient} found!")
            return True
        else:
            # print(f"{ingredient} not found")
            return False
            

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)


    def display_recipe(self):
        print(f"Recipe Name: {self.name}")
        print(f"Cooking Time: {self.cooking_time} minutes")
        print("Ingredients:")
        for ingredient in self.ingredients:
            print(f"- {ingredient}")
        print(f"Difficulty: {self.difficulty}")
        print()


    def __str__(self):
        # for ingredient in self.ingredients:
        print_ingredient = "- " + str(self.ingredients) + "\n"
        output = \
            "\nRecipe: " + str(self.name) + \
            "\nCooking Time (min): " + str(self.cooking_time) + \
            "\nIngredients: " + str(print_ingredient) + \
            "\nDifficulty: " + str(self.difficulty)
        return output
    

    def recipe_search(data, search_terms):
        """Search for recipes by ingredients and display matching ones"""
        found_recipe = False  # Flag to track if we find any matching recipes
        print(f"Searching for recipes containing: {', '.join(search_terms)}\n")

        for recipe in data:
            # Collect the search terms that match the recipe ingredients
            matching_terms = [term for term in search_terms if recipe.search_ingredients(term)]
            if matching_terms:
                found_recipe = True
                print(f"Recipe with search term(s) {', '.join(matching_terms)} found:")
                recipe.display_recipe()
        if not found_recipe:
            print(f"No recipes found containing any of the search terms: {', '.join(search_terms)}.\n")


tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 3)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
banana_smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 3)

recipes_list = [tea, coffee, cake, banana_smoothie]

print(tea)

Recipe.recipe_search(recipes_list, ["Bananas", "Water", "Sugar"])