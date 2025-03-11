"""
This script is a practices day 6 of the course of python
"""
import shutil
from pathlib import Path

# Register username
user = input("Enter a username: ")

# Recetary path (main folder)
main_folder = Path(Path.home(), "day6", "Recetary")

# Create recetary path if does not exist
if not main_folder.exists():
    main_folder.mkdir(parents=True, exist_ok=True)

# list with all categories (paths) in recetary (main folder)
categories = [f for f in main_folder.glob("*") if f.is_dir()]


def choose_category(categories):
    show_menu(categories)
    while True:
        index = input("Choose a category number: (Enter '0' to leave) ")
        if index == "0":
            break
        if index.isdigit() and 1 <= int(index) <= len(categories):
            return categories[int(index) - 1]
        else:
            print("Invalid category selection!")


def get_names_categories(categories):
    # Funcion para obtener los nombres de los path
    names_categories = []
    for category in categories:
        names_categories.append(category.name)
    return names_categories


def show_menu(categories):
    # Funcion para mostrar un menu de los path existentes en main_folder
    names_categories = get_names_categories(categories) # Obtiene un string con el nombre del path
    menu = "Categories menu:\n"
    for i, name in enumerate(names_categories, 1): # Bucle que crea el menu
        menu += f"{i}. {name}\n"
    print(menu)


def show_recipes(directory):
    recipes = list(directory.glob("*.txt"))
    if recipes:
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe.name}")
    else:
        print(f"No recipes found in this category")


def print_recipe(recipe_path):
    with open(recipe_path, "r") as file:
        content = file.read()
        print(content)


def create_recipe(directory):
    recipe_name = input("Name for the new recipe (without extension): ").strip()
    recipe_path = directory / f"{recipe_name}.txt"

    if recipe_path.exists():
        print(f"Recipe {recipe_name} already exists! Please choose another name.")
        return

    content = input("Write the content of the new recipe:\n")

    with open(recipe_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Recipe {recipe_name} has been created successfully in this category {directory.name}!.")


def create_category(main_folder):
    category_name = input("Category name (without extension): ").strip()
    new_path = main_folder / category_name

    if new_path.exists():
        print(f"This category {category_name} already exists! Please choose another name.")
        return

    new_path.mkdir(parents=True, exist_ok=True)
    print("New category has been created successfully in your recetary!.")
    return new_path


def delete_recipe(recipe_path):
    if recipe_path.exists():
        recipe_path.unlink()
        print(f"Recipe {recipe_path} has been deleted successfully!")
    else:
        print(f"Recipe {recipe_path} does not exist!")


def delete_category(category_path):
    if category_path.exists():
        if category_path.is_dir():
            shutil.rmtree(category_path)
            print(f"Category {category_path.name} has been deleted successfully!")
        else:
            print(f"{category_path.name} is not a category (it's a file)!")
    else:
        print(f"Category {category_path.name} does not exist!")


def user_iteraction(categories, main_folder, user):
    while True:
        print("\n" * 100)
        print(f"Hi {user}, welcome to {main_folder.name}!")
        print(f"\nPlease {user}, enter one option")
        print("1. Read recipe")
        print("2. Create recipe")
        print("3. Create category")
        print("4. Delete recipe")
        print("5. Delete category")
        print("6. Exit program")

        choice = input("Choose an option: ")

        if choice.isdigit():  # Check if the input is a number
            choice = int(choice)
            if choice == 1:
                print("\n" * 100)
                if not categories:  # Check if there are no categories
                    print("No categories available. Please create a category first.")
                    continue  # Return to the main loop

                category_path = choose_category(categories)  # Call the function to select a category
                if category_path is None:  # If the user exits the selection
                    continue

                show_recipes(category_path)
                recipes = list(category_path.glob("*.txt"))  # List all .txt files
                if not recipes:  # Check if there are no recipes
                    print("No recipes found in this category. Please choose another category.")
                    continue  # Return to category selection

                index_recipe = input("Choose a recipe number: (Enter '0' to leave) ")
                if index_recipe == "0":
                    continue
                if index_recipe.isdigit() and 1 <= int(index_recipe) <= len(recipes):
                    print_recipe(recipes[int(index_recipe) - 1])
                else:
                    print("Invalid recipe selection!")

            elif choice == 2:  # Create recipe
                print("\n" * 100)
                if not categories:  # Check if there are no categories
                    print("No categories available. Please create a category first.")
                    continue  # Return to the main loop

                category_path = choose_category(categories)  # Call the function to select a category
                if category_path is None:  # If the user exits the selection
                    continue

                create_recipe(category_path)  # Create a new recipe

            elif choice == 3:  # Create category
                print("\n" * 100)
                new_category = create_category(main_folder)  # Create a new category
                if new_category:
                    categories.append(new_category)  # Add the new category to the list

            elif choice == 4:  # Delete recipe
                print("\n" * 100)
                if not categories:  # Check if there are no categories
                    print("No categories available. Please create a category first.")
                    continue  # Return to the main loop

                category_path = choose_category(categories)  # Call the function to select a category
                if category_path is None:  # If the user exits the selection
                    continue

                show_recipes(category_path)
                recipes = list(category_path.glob("*.txt"))  # List all .txt files
                if not recipes:  # Check if there are no recipes
                    print("No recipes found in this category. Please choose another category.")
                    continue  # Return to category selection

                recipe_index = input("Choose a recipe number: (Enter '0' to leave) ")
                if recipe_index == "0":
                    continue
                if recipe_index.isdigit() and 1 <= int(recipe_index) <= len(recipes):
                    delete_recipe(recipes[int(recipe_index) - 1])  # Delete the selected recipe
                else:
                    print("Invalid recipe selection!")

            elif choice == 5:  # Delete category
                print("\n" * 100)
                if not categories:  # Check if there are no categories
                    print("No categories available. Please create a category first.")
                    continue  # Return to the main loop

                category_path = choose_category(categories)  # Call the function to select a category
                if category_path is None:  # If the user exits the selection
                    continue

                delete_category(category_path)  # Delete the selected category
                categories.remove(category_path)  # Remove the deleted category from the list

            elif choice == 6:  # Exit program
                print("Exiting program...")
                break

            else:
                print("Invalid option. Try again.")  # Handle invalid numeric input

        else:
            print("Invalid input. Please enter a number.")  # Handle non-numeric input


if __name__ == "__main__":
    user_iteraction(categories,main_folder,user)