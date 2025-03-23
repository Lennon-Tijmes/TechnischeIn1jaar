def main():
    while True:
        try:
            C = float(input("Celcius: "))
            print(f"Fahrenheit:{convert_c_f(C)}")
        except ValueError:
            print("Needs to be a number")
            continue


def convert_c_f(C):
    F = float((C * 1.8) + 32)
    return F



if __name__ == "__main__":
    main()
