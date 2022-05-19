import logging
from dataclasses import dataclass, fields  # Built in modules
from concurrent.futures import ThreadPoolExecutor  # Built in module

import requests
from icecream import ic

from products.etl_transform import transform_product

from products.constants import (
    ETL_EXTRACT_MAX_WORKERS,  # Number of simultaneous requests
    URL_OPEN_FOOD_FACT,
)


@dataclass(init=False)
class WellFormedProduct:  # Model used for each product to get downloaded
    _id: int
    _keywords: list
    brands: str
    categories: list
    categories_old: str
    code: int
    generic_name_fr: str
    image_thumb_url: str
    image_url: str
    ingredients_text_fr: str
    lang: str
    mega_keywords: str
    nutriments: dict
    nutriscore_grade: str
    pnns_groups_1: str
    product_name_fr: str
    quantity: str
    stores: str
    stores_tags: list
    url: str

    def __init__(self, downloaded_product):
        # Add fields to the downloading product to make it conform to this model
        downloaded_product["categories"] = [True]
        downloaded_product["mega_keywords"] = "True"
        downloaded_product["nutriments_100g"] = "True"
        
        # Below, browse all the attributes of the WellFormedProduct class
        # and put them in a tuple named "model_attributes"
        model_attributes = tuple(field.name for field in fields(self))

        # Add to the created object, the attribute "is_valid" with the value "False".
        setattr(self, "is_valid", False)

        nbr_of_model_attributes_found_in_downloaded_product = 0

        # The attributes of WellFormedProduct must be presnt in the downloaded product
        # and not empty
        for field, value in downloaded_product.items():
            if (    value
                    and field in model_attributes):

                nbr_of_model_attributes_found_in_downloaded_product +=1
                # Assign to the instance of WellFormedProduct (self) a key and its value
                setattr(self, field, value)

            if (    nbr_of_model_attributes_found_in_downloaded_product == len(model_attributes)
                    and downloaded_product["lang"] == "fr"):

                # Modify the attribute "is_valid" of the created instance (self)
                # with the new value: True.
                setattr(self, "is_valid", True)


def check_fields_of_product(product_downloaded: dict):
    """Check if all required fields of the product are present.
    Returns an instance. Not a dict!!!"""    
    if not (
            product_downloaded
            and isinstance(product_downloaded, dict)):
        return False
    return WellFormedProduct(product_downloaded)


def get_url(url):
    return requests.get(url).json()


def download_products(required_nbr_of_products: int, keyword):

    if      not (    required_nbr_of_products
                    and keyword
                    and isinstance(required_nbr_of_products, int)
                    and isinstance(keyword, str)
            or required_nbr_of_products < 1):
        return
    
    page_nbr = -9
    nbr_of_downloaded_products = 0
    while nbr_of_downloaded_products <= required_nbr_of_products:
        
        page_nbr += ETL_EXTRACT_MAX_WORKERS
        params_as_str = (
            "action=process"
            "&sort_by=unique_scan_n"
            "&page_size=20"
            "&json=1")

        word_to_find_in_product = ""
        if keyword not in ["any", "all"]:
            word_to_find_in_product = (
                "&tagtype_0=categories"
                "&tag_contains_0=contains"
                f"&tag_0={keyword}"
            )

        urls = [
            f"{URL_OPEN_FOOD_FACT}?{params_as_str}{word_to_find_in_product}"
            f"&page={page_nbr+i}" for i in range(ETL_EXTRACT_MAX_WORKERS)]
        nbr_of_empty_response = 0
        with ThreadPoolExecutor(max_workers=ETL_EXTRACT_MAX_WORKERS) as pool:
            
            list_of_responses = list(pool.map(get_url,urls))

        

        for res in list_of_responses:
            if res:
                product_not_found = not res.get("products", None)
                if product_not_found:
                    nbr_of_empty_response +=1
                    continue
                
                for downloaded_product in res['products']:
                    
                    verified_product = check_fields_of_product(downloaded_product)
                    if not (
                                verified_product
                                and verified_product.is_valid):
                        continue
                    
                    modified_product = transform_product(verified_product)
                    if not modified_product:
                        continue

                    nbr_of_downloaded_products += 1
                    
                    if nbr_of_downloaded_products > required_nbr_of_products:                    
                        return
                    # Ci-dessous, "yield" est comme un "return" sauf qu'il revient ici une fois que la fonction
                    # qui en a besoin a terminé. Ainsi, la boucle continue.
                    # L'objet généré par un yield est un générateur. Il peut être converti en liste.
                    yield modified_product
        
        if nbr_of_empty_response >= ETL_EXTRACT_MAX_WORKERS:
            
            return