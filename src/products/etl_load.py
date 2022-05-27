import logging

from django.db import transaction

from icecream import ic

from products.models import Category, Product
        

def populate_database(products: list, categories: set)->bool:
    """Populate the database with products and categories.
    Return True if everything went well otherwise False"""

    print("Quantity of products to put into the database: ", len(products))
    print()
    if not (    products
                and categories
                and isinstance(products, list)
                and isinstance(categories, set)):
        return False

    added_categories: dict = Category.add_many(categories)
    if not added_categories:
        return False

    return Product.add_many(products, added_categories)