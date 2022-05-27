import copy

import pytest

from products.models import Category
from products.models import Product as SUT
from src.tests.products.params_for_mark_parametrize.products_objs import (
    dl_product1,
    dl_product2,
)

products = [dl_product1, dl_product2]

# Create a virtual database then destroy it after all tests have finished.
pytestmark = pytest.mark.django_db


categories_dict = {} # keys will be names, values will be instances of Category

@pytest.fixture
def categories_as_dict():
     # Create categories so that a product can be added and get included in a stored category
    categories = [category for product in products for category in product.categories]
    
    
    for category in categories:
        categories_dict[category] = Category.objects.create(name=category)

    return categories_dict

@pytest.fixture
def add_products_to_db(categories_as_dict):  
    SUT.add_many(products, categories_as_dict)


class TestProductModel:

    def test_add_many(self, caplog, categories_as_dict):
        caplog.clear()

        print("A list of elements that are not instances of WellFormedProduct should raise "
            " an exception and return False because it can't be stored in the database.")
        assert SUT.add_many(
            ["not", "list", "of", "instance", "of", "WellFormedProduct"],
            categories_as_dict
            ) == False
        assert caplog.text != None
        caplog.clear()

        print("Stored_categories that is not a dict with instances of Category as values "
            "should return False because it can't be stored in the database.")
        assert SUT.add_many(
            products,
            {"cat1": "cat1", "cat2": "cat2", "cat3": "cat3", "cat4": "cat4", "cat5": "cat5"},
            ) == False
        assert caplog.text == ""

        print("A list of welformed products and a dict containing categories that are already stored "
            "in the database should store all of the products then return True.")
        assert SUT.add_many(
            products,
            categories_as_dict
            ) == True
        
        assert SUT.objects.all().count() == 2

    @pytest.mark.test_me
    def test_find_original_products(self, add_products_to_db):

        product1 = copy.deepcopy(dl_product1)
        product2 = copy.deepcopy(dl_product1)

        product1._id = "123456"
        product1.product_name_fr = "Lemonade"
        product1.mega_keywords = " lemonade lemon sugar beverage "

        product2._id = "123457"
        product2.product_name_fr = "Cool cola"
        product2.mega_keywords = " cool cola soda beverage cola "

        two_products = [product1, product2]
        categories_as_dict   # To create categories_dict

        SUT.add_many(two_products, categories_dict)      

        print(
            "'beverage' as keyword should return all products containing the keyword 'beverage'")
        
        original_products = SUT.find_original_products("beverage")
        assert len(original_products) == 2

        print(
            "'beverage orange' as keywords should return an empty Queryset because no product "
            "contains ALL these keywords (None of the products contains 'orange' AND 'beverage'"
            " in keywords)")
        
        original_products = SUT.find_original_products("beverage orange")
        assert list(original_products) == []

        print(
            "'beverage lemon' as keywords should return only one product because only one "
            "product contains ALL these keywords")
        
        original_products = SUT.find_original_products("beverage lemon")
        assert len(original_products) == 1
        assert original_products[0].name == "Lemonade"


