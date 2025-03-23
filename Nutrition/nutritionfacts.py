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


def main():
    fruit = input("Fruit: ").strip().lower()
    calories = get_calories(fruit)
    if calories is not None:
        print(f"Calories: {calories}")

if __name__ == "__main__":
    main()
