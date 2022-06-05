from django.test import Client

import pytest

from products.models import Product
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

@pytest.mark.django_db

@pytest.mark.test_me
def test_get_substitutes(monkeypatch, caplog):

    def mock_find_substitute_products(id, nutriscore_grade):
        try:
            print("Dans le mock")
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

    print("An original product")
    print("     should return a list of products with a better  nutriscore_grade")
    # assert "Render a list of substitute_products with better nutriscore_grade" in caplog.text
    response = client.get('/get-substitutes', {'id': '123456', 'nutriscore_grade': "c"})
    print()
    print()
    for product in response.context["substitute_products"]:
        assert product["nutriscore_grade"] < "c"
