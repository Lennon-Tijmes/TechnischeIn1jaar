from nutritionfacts import get_calories

def test_spaces_sweet_cherries():
    assert get_calories("sweet cherries") == 100

def test_capitilazation_ApPLe():
    assert get_calories("ApPLe") == 130

def test_nothing():
    assert get_calories("") == 0

def test_banana_Apple():
    assert get_calories("Banana Apple") == 0

def test_numbers():
    assert get_calories(15) == 0

def test_special_characters():
    assert get_calories("!@#$!") == 0