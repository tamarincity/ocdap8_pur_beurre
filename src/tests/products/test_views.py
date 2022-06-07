from django.test import Client

import pytest

from products.models import Category, Product
import src.products.views as SUT




client = Client()

class MockRequest:
    def __init__(self):
        self.GET = {}

request = MockRequest()



substitutes_list1 = [
    {"id": 12312311,
    "nutriscore_grade": "b",
    "name": "substitute product name 1",
    "weight": 4},
    {"id": 12312312,
    "nutriscore_grade": "b",
    "name": "substitute product name 2",
    "weight": 3},
    {"id": 12312313,
    "nutriscore_grade": "a",
    "name": "substitute product name 3",
    "weight": 2}]

substitutes_list2 = [
    {"id": 12312311,
    "nutriscore_grade": "a  ",
    "name": "substitute product name 1",
    "weight": 4},
    {"id": 12312312,
    "nutriscore_grade": "a",
    "name": "substitute product name 2",
    "weight": 3},
    {"id": 12312313,
    "nutriscore_grade": "a",
    "name": "substitute product name 3",
    "weight": 2}]


def add_a_category():
    return Category.objects.create(name="Category name")


def add_a_product():
    return Product.objects.create(
        name="Product name",
        brands="brand1, brand2",
        code=8714100614754,
        original_id=9876543210,
        quantity="Quantity 1.5l",
        image_thumb_url="url-thumb-image",
        image_url="url-thumb-image",
        ingredients_text="list of ingredients",
        keywords="some keywords (mega key_words)",
        nutriments="Some nutriments",
        nutriscore_grade="c",
        stores="All the stores where you can find the product",
        url="url_of_the_website_of_the_product",
    )

@pytest.mark.django_db
@pytest.mark.test_me
def test_get_substitutes(monkeypatch, caplog):
    caplog.clear()

    def mock_find_substitute_products(id, nutriscore_grade):
        try:
            if not (id
                    and isinstance(id, str)):
                raise Exception("id must be string and not empty")
            if not (nutriscore_grade
                    and isinstance(nutriscore_grade, str)):
                raise Exception("nutriscore_grade must be string and not empty")
            int(id)
        except Exception as e:
            print("Exception raised: e")


        if nutriscore_grade > "b":
            return substitutes_list1

        if nutriscore_grade == "b":
            return substitutes_list2

        return []

    
    monkeypatch.setattr(Product, "find_substitute_products", mock_find_substitute_products)

    print("An original product id that doesn't exist should raise an exception")
    with pytest.raises(Exception):
        response = client.get('/get-substitutes', {'id': '9995288', 'nutriscore_grade': "c"})

    print("An original product")
    print("     should return a list of products with a better  nutriscore_grade")
    
    caplog.clear()
    add_a_category()
    add_a_product()
    response = client.get('/get-substitutes', {'id': '1', 'nutriscore_grade': "c"})
    print()
    print()
    for product in response.context["substitute_products"]:
        assert product["nutriscore_grade"] < "c"
