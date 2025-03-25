# Make a small program that can get the first unique letter in a word or sentence.


def first_unique_char(text):
    char_count = {}
    text = text.lower()

    for char in text:
        if char != " ": # Don't look at the spaces
            char_count[char] = char_count.get(char, 0) + 1
    
    for char in text: 
        if char != " " and char_count[char] == 1:
            return char

    return None