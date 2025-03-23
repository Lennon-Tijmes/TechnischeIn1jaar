from bank import value

def test_hey():
    assert value("Hey how are you") == 20

def test_hello():
    assert value("Hello can I have money?") == 0

def test_numbers():
    assert value("100 dollar please") == 100

def test_special_characters():
    assert value("!#$%") == 100

def test_hhhello():
    assert value("hhhhhhhhhello") == 20

def test_starting_with_blank_space():
    assert value(" Hello") == 0