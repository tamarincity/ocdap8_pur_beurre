from pprint import pprint
import logging

from icecream import ic

from products.utils import WellFormedProduct
from products import utils
from .constants import (
    PRODUCT_NAME_MAX_LENGTH,
    QUANTITY_MAX_LENGTH,
    UNWANTED_CATEGORIES,
)


def str_to_list(string: str) -> list:
    """Convert string to list using "," as a separator"""
    
    if not (
            string
            and isinstance(string, str)):
        logging.warning("Arg in str_to_list must be a string and not empty!")
        return None
        
    elements = string.split(',')    
    elements = [element.strip().capitalize() for element in elements]
    
    return elements


def remove_products_with_unwanted_categories(categories: list[str]) -> list[str]:    
    if not categories:
        return None
    if not isinstance(categories, list):
        raise TypeError

    categories = [category for category in categories if category]

    for unwanted_category in UNWANTED_CATEGORIES:
        if unwanted_category in categories:
            
            return None
    
    return categories


def add_mega_keywords_to_product(product: WellFormedProduct):
    
    if not (    product
                and isinstance(product, WellFormedProduct)):

        raise Exception("Error in products.etl_transform add_mega_keywords_to_product()"
            ": product must be an instance of WellFormedProduct")
        
    keywords = " ".join(product._keywords)
    
    mega_keywords = (
        product.product_name_fr
        + " " + product.quantity
        + " " + product.brands
        + " " + product.generic_name_fr
        + " " + product.categories_old
        + " " + keywords
        + " " + str(product.code))
    
    mega_keywords = utils.format_text(mega_keywords)
    
    product.mega_keywords = mega_keywords
    
    return product


def transform_product(product):
    
    categories_as_string = (
        product.categories_old.replace("Aliments et boissons ", "")
            .replace(" & ", " et ")
            .replace("&", " et "))

    categories_as_list = str_to_list(categories_as_string)    
    if not categories_as_list:        
        return None
    
    categories_as_list = remove_products_with_unwanted_categories(categories_as_list)    
    if not categories_as_list:        
        return None
    
    setattr(product, "categories", categories_as_list)
    setattr(product, "categories_old", categories_as_string)

    if len(product.product_name_fr) > PRODUCT_NAME_MAX_LENGTH:
        product.product_name_fr = product.product_name_fr[:PRODUCT_NAME_MAX_LENGTH - 3] + "..."
    if len(product.quantity) > QUANTITY_MAX_LENGTH:
        product.quantity = product.quantity[:QUANTITY_MAX_LENGTH - 3] + "..."
    product = add_mega_keywords_to_product(product)
    
    return product


def fetch_all_categories_from_products(products):
    return set(category for product in products for category in product.categories)