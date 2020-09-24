import pytest

from steganossaurus.binary_manipulation import substitute_lsb, extract_lsb

def test_substitute_lsb():
    assert substitute_lsb(200, "11") == 203
    assert substitute_lsb(129, "1100") == 140

    with pytest.raises(ValueError) as info:
        substitute_lsb(4, "1101")    
    assert str(info.value) == "New value is too big to be encoded inside origin value."

    with pytest.raises(TypeError):
        substitute_lsb("banana", "1010")

    with pytest.raises(ValueError) as info:
        substitute_lsb(200, 10)
    assert str(info.value) == "New value must be a string with a binary encoded number value."

def test_extract_lsb():
    assert extract_lsb(10, 2) == '10'
    assert extract_lsb(11, 2) == '11'
