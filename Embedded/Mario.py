while True:
    n = int(input("Height: "))
    if n > 0 and n < 9:
        break

for i in range(n):
    # Print blank space,    first hash,     Blank space, hash
    print(" " * (n - 1 - i) + "#" * (1 + i) + "  " + "#" * (i + 1))