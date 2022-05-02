import logging

from django.db import transaction

from icecream import ic

from products.models import Category, Product


def add_categories(categories: list)->dict:
    """Add categories to the database and return a dictionary that contains
    each stored category as an object.
    E.g.: stored_categories["Beverage
    If somenthing went wrong, return None"""

    if not ( categories and isinstance(categories, set)):
        return None

    stored_categories = {}
    try:
        with transaction.atomic():  # Commit only if all queries have been done with success
            for category in categories:
                try:
                    stored_categories[category] = Category.objects.get(name=category)
                except Category.DoesNotExist:  # If the category has not been already stored
                    stored_categories[category] = Category(name=category)
                    stored_categories[category].save()
                except Exception as e:
                    raise Exception(
                        "probably several categories have been stored in the database "
                        "with the same name")
        return stored_categories
    except Exception as e:
        logging.error("Error adding categories. Exception was: %s", e)



def add_products(products: list, stored_categories: dict)->bool:
    """Add products to the database then return True if they were added successfully
    otherwise False"""
    if not (    products
                and stored_categories
                and isinstance(products, list)
                and isinstance(stored_categories, dict)):
        return False

    is_new_product_added = False
    try:
        with transaction.atomic():  # Commit only if all queries have been done with success
            for product in products:
                try:
                    stored_product = Product.objects.get(original_id=product._id)
                except Product.DoesNotExist:  # if the product is not already stored
                    is_new_product_added = True
                    stored_product = Product(
                            image_thumb_url=product.image_thumb_url,
                            image_url=product.image_url,
                            ingredients_text=product.ingredients_text_fr,
                            keywords=product.mega_keywords,
                            name=product.product_name_fr,
                            nutriments=product.nutriments,
                            nutriscore_grade=product.nutriscore_grade,
                            original_id=product._id,
                            quantity=product.quantity,
                            stores=product.stores,
                            url=product.url,
                            )
                    stored_product.save()
                except Exception as e:
                        raise Exception(
                            "Probably several products have been stored in the database "
                            "with the same original_id")

                for category in product.categories:
                    stored_category = Category.objects.get(name=category)
                    stored_category.products.add(stored_product)

        if not is_new_product_added:
            print("No new product added to the database!")
        return True
    except Exception as e:
        logging.error("Error adding products. Exception was: %s", e)
        return False
        

def populate_database(products: list, categories: set)->bool:
    """Populate the database with products and categories.
    Return True if everything went well otherwise False"""
    ic()
    print("categories to put into the database: ", categories)
    print("Length of products to put into the database: ", len(products))
    print()
    if not (    products
                and categories
                and isinstance(products, list)
                and isinstance(categories, set)):
        return False
    ic()
    added_categories: dict = add_categories(categories)
    if not added_categories:
        return False
    ic()
    return add_products(products, added_categories)