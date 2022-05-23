import pytest

from products import etl_transform as SUT
from products.constants import (
    UNWANTED_CATEGORIES,
)


def test_str_to_list(caplog):

    str_to_turn_into_list = "category1,caTegory2,    category3, CATEGORY4"
    expected = ['Category1', 'Category2', 'Category3', 'Category4']

    print("None as string to turn into list: ")
    print("     should return None")
    assert SUT.str_to_list(None) == None
    print("     should log a warning")
    assert "WARNING" in caplog.text

    print("Non string as string to turn into list: ")
    print("     should return None")
    assert SUT.str_to_list(["not", "a", "string"]) == None
    print("     should log a warning")
    assert "WARNING" in caplog.text

    print("""Words separated by space should return all the words as one element of a list.
    All the words should be lower case except for the first one
    that should be capitalized""")
    assert SUT.str_to_list("word1 word2   WORD3") == ["Word1 word2   word3"]

    print("Words separated by coma should return a list of capitalized words.")
    assert SUT.str_to_list(str_to_turn_into_list) == expected

@pytest.mark.test_me
def test_remove_products_with_unwanted_categories():


    print("No categories should return None so the product should be removed")
    assert SUT.remove_products_with_unwanted_categories("") == None

    print("Non list as categories should raise TypeError")
    with pytest.raises(TypeError):
        SUT.remove_products_with_unwanted_categories("cat1, cat2, cat3")

    print("""Any of an unwanted category in a list of categories 
    should return None so the product should be removed""")
    for unwanted_category in UNWANTED_CATEGORIES:
        assert SUT.remove_products_with_unwanted_categories(
            [unwanted_category, "good category"]) == None

    print("""A list of categories with some empty categories 
    should return the list without the empty categories""")
    assert SUT.remove_products_with_unwanted_categories(
        ["cat1", "", "cat2", None]) == ['cat1', 'cat2']