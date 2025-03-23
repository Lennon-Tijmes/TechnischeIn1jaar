from twttr import shorten

def test_caps():
    assert shorten("TWITTER") == "TWTTR"
    assert shorten("AVCDEF") == "VCDF"

def test_low():
    assert shorten("twutterauo") == "twttr"

def test_special_char():
    assert shorten("!@#$%!@#$") == "!@#$%!@#$"

def test_aaaaaaaaaaaaa():
    assert shorten("aaaaaaaaaaaaa") == ""

def test_empty():
    assert shorten("") == ""

def test_numbers():
    assert shorten("1234") == "1234"