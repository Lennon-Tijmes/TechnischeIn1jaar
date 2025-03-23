def main():
    message = input("input: ")
    print("output", shorten(message), sep="")

def shorten(word):
    shorten_word = ""
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for m in word:
        if m not in vowels:
            shorten_word = shorten_word + m
    
    return shorten_word

if __name__ == "__main__":
    main()
