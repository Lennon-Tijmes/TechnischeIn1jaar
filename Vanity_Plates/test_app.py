from app import is_valid

def test_cs50_true():
    assert is_valid("cs50") == True

def test_cs05_false():
    assert is_valid("CS05") == False

def test_AAAAAAAA_false():
    assert is_valid("AAAAAAAA") == False

def test_PI314_false():
    assert is_valid("PI3.14") == False

def test_OUTATIME_false():
    assert is_valid("OUTATIME") == False