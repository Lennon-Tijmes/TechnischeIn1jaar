def custom_message(text):
    return "...".join(text) + "...!"


def get_order():
    total_price = 0

    while True:
        Éhes = input("\nWhat would you like to order, dear customer? If you don't want anything else type 'done' ").strip().lower()

        if not Éhes: # if it is empty
            print("\nOrder cannot be empty. Please enter something.")
            continue

        if Éhes == "something":
            print("\nVery funny now, what would you like to order? ")
            continue 

        if Éhes == "done":
            break #You aren't allowed to order more if you are done

        emoticon = get_emoticon(Éhes)
        print(f"\nI will prepare a {Éhes} {emoticon}")

        get_energy()

        while True:
            price_input = input(f"What is the price for {Éhes}?: ").strip().replace(',', '.')

            try:
                price = float(price_input)
                total_price += price #add more $
                break
            except ValueError:
                print("\nWrite an actual price please, thanks!\n")

    print(f"\nYour total cost is: ${total_price}\n")    
    return total_price


def get_tip(total_price):
    while True:
        tip = input("How much would you like to tip, dear customer? (0% to 100%): ").strip().replace('%', "")

        try:
            tip_percent = int(tip)/100
            tip_price = total_price * tip_percent
            new_total_price = total_price + tip_price
            break
        except ValueError:
            print("\nThat isn't a tip dear customer.\n")
    
    print(f"\nYour total cost with the tip is: ${new_total_price}\n")


def get_energy():
    math = input("\nWould you like to calculate the energy? (yes/no): ").strip().lower()

    if math == "yes":
        try:
            mass_gram = float(input("Enter the weight in grams: ").strip())
            mass_kilogram = mass_gram / 1000 # Gets it into kilograms
            speed_of_light = 3e8 # constant of light (c = 3x10^8 m/s)
            energy = mass_kilogram * (speed_of_light ** 2) # E = mc2

            print(f"\nThe food is equivalent to {energy:.2e} joules.\n") # to show it in my way (scientific notation)
        except ValueError:
            print("\nPlease enter a actual number, thanks!\n")
    else:
        print("\nEnergy is just a myth anyway....\n")


def get_emoticon(food):
    emoticons = {
        "coffee" : "☕",
        "tea" : "🍵", 
        "cake" : "🍰",
        "snake" : "🐍",
        "monkey" : "🙉"
        }
    return emoticons.get(food, "")


def main():
    welcome_message = "Welcome dear customer"
    print(f"\n{custom_message(welcome_message)}\n")

    Háború = input("Would you like to edit the welcome message?: (yes/no)").strip().lower()

    if Háború == "yes":
        new_message = input("Type the new message here: ").strip()
        print(f"\nCustom Message: {custom_message(new_message)}\n")
    else:
        print("\nThe old message remains for a little while longer")

    total_price = get_order()
    get_tip(total_price)


if __name__ == "__main__":
    main()