import logging

from icecream import ic

from ..constants import (
    UNWANTED_CATEGORIES,
    REQUIRED_FIELDS_OF_A_PRODUCT,
)


def are_all_fields_in_product(product):
    """Check if all required fields are present and not null in product"""

    if not (
        product
        and isinstance(product, dict)):
        logging.warning("Warning: product must be a dict!")
        return False
    
    for required_field in REQUIRED_FIELDS_OF_A_PRODUCT:
        if required_field not in product.keys():
            logging.warning("At least one required field is missing in product")
            return False
        if not product[required_field]:  # If the value of required field is empty or null
            logging.warning("At least one value of the required fields is missing in product")
            return False

    return True


def str_to_list(string: str):
    """Convert string to list using ", " as separator"""
    if not (
            string
            and isinstance(string, str)):
        logging.warning("Arg in str_to_list must be a string and not empty!")
        return None
    try:
        elements = string["categories_old"].split(', ')
        elements = [element.strip() for element in elements]
        return elements
    except Exception as e:
        logging.error("Error: unable to parse categories!")
        logging.error(str(e))
        return None


def transform_data(rough_products: list):
    """Transform data to be more manageable"""

    if not isinstance(rough_products, list):
        logging.error("Error: Data to transform must be a list!")
        raise Exception("Error: Data to transform must be a list!")

    products = []
    for product in rough_products:
        if not isinstance(product, dict):
            logging.error("Error: Product must be a dict!")
            continue

        if not are_all_fields_in_product(product):
            continue

        categories = str_to_list(product.get('categories_old', None))
        if not categories:
            continue

        if product["lang"] != "fr":
            continue

        # Seek for bad categories
        for unwanted_category in UNWANTED_CATEGORIES:
            if unwanted_category in categories:
                continue

        product["categories"] = categories
        products.append(product)

    if not products:
        logging.warning("No products found!")
    

    return products
