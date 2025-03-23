import random

a = b = c = d = e = f = g = h = i = j = False

def main():
    global a, b, c, d, e, f, g, h, i, j
    print("Welcome to the Survival Simulator!")
    print("You are in an abandoned supermarket and must solve puzzles to escape!")

    while not all([a,b,c,d,e,f,g,h,i,j]):
        print("\nChoose an option:")
        print("1. File Extensions: What's in this file?")
        print("2. Math Interpreter: Unlock the safe")
        print("3. Nutrition Facts: Prepare a meal")
        print("4. Coke Machine: Get the right combination")
        print("5. CamelCase Decoder: Decode the message")
        print("6. Emojize: Guess the clue")
        print("7. Guessing Game: Guess the secret code")
        print("8. Bitcoin Price Index: Choose whether to invest in Bitcoin")
        print("9. felipes_taqueria: Make your taco")
        print("10. Outdated: The milks spoils")
        print("11. Exit")

        choice = input("Make a choice (1-11): ")
        if choice == "11":
            break
        else:
            options(choice)

    if all([a,b,c,d,e,f,g,h,i,j]):
        adieu()
        exit(1)


def options(choice):
    global a,b, c, d, e, f, g, h, i, j
    match choice:
        case "1":
            file_extensions()
            a = True
        case "2":
            math_interpreter()
            b = True
        case "3":
            nutrition_facts()
            c = True
        case "4":
            coke_machine()
            d = True
        case "5":
            camelcase_decoder()
            e = True
        case "6":
            emojize()
            f = True
        case "7":
            guessing_game()
            g = True
        case "8":
            bitcoin_price_index()
            h = True
        case "9":
            felipes_taqueria()
            i = True
        case "10":
            outdated()
            j = True
        case _:
            print("Invalid choice")


# Numero uno 1 A
def file_extensions():
    extensions = {"jpg": "image", "pdf": "document", "text": "text"}
    file_ext = random.choice(list(extensions.keys()))
    print(f"You find a file named 'recipe.{file_ext}'.")
    while True:
        user_input = input("Type the file name to check its extension: ")
        if user_input == f"recipe.{file_ext}":
            print(f"This is a {extensions[file_ext]} file containing a recipe")
            break
        else:
            print("Unknown file type! Try again.")


def help_math(expression, operator):
    for i, element in enumerate(expression):
        if element == operator:
            if operator == "/" and expression[i+1] == "0":
                print("Cannot devide by 0!")
                return None
            left_operand = float(expression[i-1])
            right_operand = float(expression[i+1])
            if operator == "*":
                result = left_operand * right_operand
            elif operator == "/":
                result = left_operand / right_operand
            elif operator == "+":
                result = left_operand + right_operand
            elif operator == "-":
                result = left_operand - right_operand
            expression[i-1] = str(result)
            del expression[i:i+2]
            break


# Zwei 2 B
def math_interpreter():
    print("A safe unlocks only with the correct calculation.")
    while True:
        expression = input("Enter maths (2 + 1 * 2): ").strip()
        things = expression.split()
        while len(things) > 1:
            while "*" in things or "/" in things:
                if "*" in things:
                    help_math(things, "*")
                elif "/" in things:
                    help_math(things, "/")
            while "+" in things or "-" in things:
                if "+" in things:
                    help_math(things, "+")
                elif "-" in things:
                    help_math(things, "-")
        print(f"The result is: {things[0]}. The safe opens waaait whaat?")
        break


# helper function for nutrition
def get_calories(fruit):
    if not isinstance(fruit, str):
        return 0
    
    nutrition_facts = {
        "apple": 130,
        "avocado": 50,
        "banana": 110,
        "cantaloupe": 50,
        "grapefruit": 60,
        "grapes": 90,
        "honeydew melon": 50,
        "kiwifruit": 90,
        "lemon": 15,
        "lime": 20,
        "nectarine": 60,
        "orange": 80,
        "peach": 60,
        "pear": 100,
        "pineapple": 50,
        "plums": 70,
        "strawberries": 50,
        "sweet cherries": 100,
        "tangerine": 50,
        "watermelon": 80
    }

    return nutrition_facts.get(fruit.lower(), 0)           


# Drie 3 C
def nutrition_facts():
    target_calories = 400
    available_fruits = ["apple", "avocado", "banana", "cantaloupe", "grapefruit", "grapes", 
                        "honeydew melon", "kiwifruit", "lemon", "lime", "nectarine", "orange", 
                        "peach", "pear", "pineapple", "plums", "strawberries", "sweet cherries", 
                        "tangerine", "watermelon"]
    
    print(f"Your goal is to get {target_calories} calories for your meal!")
    print("Availabe fruits:")
    print(", ".join(available_fruits))

    total_calories = 0
    selected_fruits = []

    while total_calories < target_calories:
        fruit = input(f"Select a fruit to add to your meal (currently you have: {total_calories} calories): ").strip().lower()

        if fruit in available_fruits:
            fruit_calories = get_calories(fruit)
            if fruit_calories == 0:
                print("Don't know that fruit. Try again!")
            else:
                selected_fruits.append(fruit)
                total_calories += fruit_calories
                print(f"{fruit.capitalize()} added: {fruit_calories} calories")
                print(f"Total calories so far: {total_calories} calories.")
        else:
            print("Choose a fruit from the list")
        
        if total_calories >= target_calories:
            print(f"Congrats! Your meal is ready with {total_calories} calories!")


# Four 4 D
def coke_machine():
    correcto_mundo = ["A", "B", "C", "D"]
    random.shuffle(correcto_mundo)
    print(f"{correcto_mundo}")
    print("You find a mysterious vending machine. Press the correct buttons to get a drink!")
    while True:
        user_input = input("Enter the code (A, B, C, D): ").strip().upper().split()
        if user_input == correcto_mundo:
            print("You hear rumbling, and a small can of unknown liquid drops down!")
            break
        else:
            print("Some dust falls down...... Try again.")


# Öt 5 E
def camelcase_decoder():
    message = "RunYouFoolDontLookBack"
    print(f"You find a message: '{message}'")
    while True:
        user_input = input("Type the decoded message: ")
        if user_input == message:
            print("Decoded message: Run You Fool Dont Look Back")
            break
        else:
            print("That ain't it chief, try again.")


# Six 6 F
def emojize():
    emojis = {"🍎": "apple", "🍌": "banana", "🍪": "cookie", "🌽": "corn", "🦆": "duck"}
    secret_emojis = random.sample(list(emojis.keys()), 3)
    print(f"You find a clue: {' '.join(secret_emojis)}")
    while True:
        user_input = input("Guess the food names: ").lower().split()
        if user_input == [emojis[e] for e in secret_emojis]:
            print("You got a key, it's a bit sticky...")
            break
        else:
            print("Wrong! Try again.")


# 777777 G
def guessing_game():
    secret_number = random.randint(1, 10)
    attempts = 3
    print("Guess the code (1-10).")
    while attempts > 0:
        try:
            user_input = int(input(f"Guess ({attempts}) attemps left): "))
            if user_input == secret_number:
                print("The door slowly opens, you did it!")
                break
            elif user_input != secret_number:
                print("Beep boop it is wrong!")
                attempts -= 1
        except ValueError:
            print("Enter a number!")


# Eight 8 H
def bitcoin_price_index():
    print("You see a sign that says 'BUY BITCOIN!!'")
    print("It looks like Bitcoin is cool, but what is its price?")
    print("You feel like it should be between 10000 and 80000, but you are unsure..")

    price = random.randint(10000, 80000) # Big numbers

    try:
        user_input = int(input("Enter the estimated price: ").replace("$", "").replace("€", ""))

        if abs(user_input - price) <= 5000:
            print(f"Good enough.. The price was €{price}. You invest wisely.")
        else:
            print(f"Well.... you are poor now. It was €{price}. It was a bit off..")
    except ValueError:
        print("That's not a number, oh.. the price changed again.")


# Nein 9 taco taco I
def felipes_taqueria():
    ingredients = ["tortilla", "beef", "chicken", "lettuce", "cheese", "salsa", "onion", "lime", "love"]
    print("🌮 Make a TACOOOOO! Choose 3 ingredients.")
    chosen_ingredients = []
    while len(chosen_ingredients) < 3:
        user_input = input("Choose your item!: ").lower()
        if user_input in ingredients and user_input not in chosen_ingredients:
            chosen_ingredients.append(user_input)
            print(f"Goooood yum {user_input.capitalize()} added!")
        elif user_input in ingredients:
            print("Don't want extra of that, say something else!")
        else:
            print("Not a good ingredient. Gimme another one pls.")

    print(f"Your taco is ready: {', '.join(chosen_ingredients)}. Enjoy!")


#10 spoiled milk J
def outdated():
    print("You find some great groceries. But some of them are expired!")
    print("Survival in this supermarket is hard, you only want fresh food.")
    
    groceries = {"milk" : "expired", "yogurt" : "expired", "cheese": "fresh", "bread": "fresh",
        "apple": "fresh", "banana": "fresh", "eggs": "expired", "carrots": "fresh", "chicken": "expired",
        "fish": "expired", "chocolate": "fresh"}
    
    fresh_items = [item for item, status in groceries.items() if status == "fresh"]
    expired_items = [item for item, status in groceries.items() if status == "expired"]

    selected_fresh = [] # Cool set empty till its filled

    print("What can I scavange?: ")
    print(", ".join(groceries.keys()))

    while len(selected_fresh) < 4:
        item = input("Pick something: ").strip().lower()

        if item in fresh_items and item not in selected_fresh:
            selected_fresh.append(item)
            print(f"{item.capitalize()} succesfully obtained! I want more!!")
        elif item in fresh_items:
            print("Mhmmm already have that, I should get something else.")
        elif item in expired_items:
            print(f"Uhhh... {item.capitalize()} is expired and smells.. I don't want that!")
        else:
            print(f"I don't see any {item.capitalize()}")
    
    print("I think I have enough fresh items, I should move on!")


# Goodbye
def adieu():
    names = []
    print("Say your totally serious escape speech!")
    print("Enter the names one by one. Type 'done' when finished")
    while True:
        name = input("Enter the name. Type 'done' to finish: ").strip()
        if name.lower() == "done":
            break
        elif name:
            names.append(name)
    
    if names:
        if len(names) > 1:
            farewell_message = f"Adieu, adieu, to {', '.join(names[:-1])}, and {names[-1]}!"
        else:
            farewell_message = f"Adieu, adieu, to {names[0]}!"
        print(f"You scream on top of your lungs!: {farewell_message}")
    else:
        print("An awkward silence arised. You should say something..")


if __name__ == "__main__":
    main()