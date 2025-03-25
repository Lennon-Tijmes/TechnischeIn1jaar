from FirstWord import first_unique_char

def test_first_unique_char():
    assert first_unique_char("swiss") == "w", "Test 1 Failed"
    assert first_unique_char("hello") == "h", "Test 2 Failed"
    assert first_unique_char("racecar") == "e", "Test 3 Failed"
    assert first_unique_char("aabbcc") == None, "Test 4 Failed"  # No unique characters
    assert first_unique_char("a") == "a", "Test 5 Failed"  # Single letter
    assert first_unique_char("") == None, "Test 6 Failed"  # Empty string
    assert first_unique_char("pneumonoultramicroscopicsilicovolcanoconiosis") == "e", "Test 7 Failed"
    assert first_unique_char("I have seen that a muffin sleeps") == "v", "Test 8 Failed"

    print("All tests passed!")

test_first_unique_char()
