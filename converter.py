def main():
    temperature = float(input("Input Fahrenheit: "))
    print("output: ", convert(temperature), sep="")


def convert(temp):
    temp = (temp * 1.8) + 32

    return temp


if __name__ == "__main__":
    main()
    