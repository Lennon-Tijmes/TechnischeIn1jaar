import random
print(random.__file__)  # Should now point to a folder, not a .py file!

def emojize():
    emojis = {"🍎": "apple", "🍌": "banana", "🍪": "cookie", "🌽": "corn", "🦆": "duck"}
    secret_emojis = random.sample(list(emojis.keys()), 3)  # ✅ Pick 3 emojis

    print(f"You find a clue: {' '.join(secret_emojis)}")  # ✅ Display emojis correctly
    while True:
        user_input = input("Guess the food names: ").lower().split()
        if user_input == [emojis[e] for e in secret_emojis]:  # ✅ Correctly map emoji to food
            print("You got a key, it's a bit sticky...")
            break
        else:
            print("Wrong! Try again.")

# Run the function to test it
emojize()
