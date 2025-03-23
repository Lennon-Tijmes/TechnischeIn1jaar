from unit_test_battle import convert_c_f
import pytest

def test_decimal_number():
    assert convert_c_f(12.5) == 54.5

def test_convert_10():
    assert convert_c_f(10.0) == 50.0

def test_convert_special_character():
    with pytest.raises(TypeError):
        convert_c_f("2#4")

def tesst_convert_text():
    with pytest.raises(TypeError):
        convert_c_f("Hello, world")
