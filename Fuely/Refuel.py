def main():
    while True:
        try:
            fraction = input("Fraction: ")
            percentage = convert(fraction)
            print(gauge(percentage))
            break
        except (ValueError, ZeroDivisionError):
            pass

def convert(fraction):
    parts = fraction.split("/")

    if len(parts) != 2:
        raise ValueError("Input is in a wrong format")
    
    try:
        x, y = int(parts[0]), int(parts[1])

        if y == 0:
            raise ZeroDivisionError("It cannot be 0")
        if x > y:
            raise ValueError("It cannot be greater")
        
        return round((x / y) * 100)
    
    except ValueError:
        raise ValueError("Both need to be int")
    except ZeroDivisionError:
        raise ZeroDivisionError("It cannot be 0")


def gauge(percentage):
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"

if __name__ == "__main__":
    main()