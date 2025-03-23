from Refuel import convert, gauge

def test_convert_valid():
    assert convert("1/2") == 50
    assert convert("3/4") == 75
    assert convert("1/4") == 25
    assert convert("99/100") == 99
    assert convert("0/1") == 0