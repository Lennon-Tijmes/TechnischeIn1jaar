Data = "Hello World"
Meow = "gibberish@meow.nl"
Testing = "I, like. to talk to Hungarians!"

#Data = Data.split(" ") # Hello World
Data = Data.replace("o", "a") # Hella Warld

if "@" in Meow:
    print("Yes") #if it is in the String

dot_count = Meow.count(".") # gibes amount :)

at_position = Meow.find("@") # Gives the position

starts_with_gib = Meow.startswith("gibberish") # returns True
end_with_nl = Meow.endswith(".nl") # True if it ends with it

Reverse = Data[::-1].lower() # Reverses and makes it lower

def word_test(sentence):
    remove = [",", ".", "?", "!"]
    for r in remove:
        sentence = sentence.replace(r, "")
    return sentence.split()


def count_vowels(sentence):
    vowels = "aeiouAEIOU"
    count = 0
    for char in sentence:
        if char in vowels:
            count += 1
    return count

# return max(words, key=len)

print(count_vowels("Pretty lady"))
print(Data)
print(Meow)

print(dot_count)
print(at_position)

print(starts_with_gib)
print(end_with_nl)
print(Reverse)

Testing = word_test(Testing)
print(Testing)