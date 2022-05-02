import logging
from dataclasses import dataclass, fields  # Built in modules
from concurrent.futures import ThreadPoolExecutor  # Built in module

import requests
from icecream import ic

from products.etl.transform import (
    remove_products_with_unwanted_categories,
    transform_product,
)

from products.constants import (
    NBR_OF_PAGES,
    URL_OPEN_FOOD_FACT,
    REQUIRED_FIELDS_OF_A_PRODUCT,
)


@dataclass(init=False)
class WellFormedProduct:
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
        
        # Ci-dessous, parcours tous les attributs de la classe WellFormedProduct et les met dans un tuple nommé "model_attributs"
        model_attributs = tuple(field.name for field in fields(self))  # => Tous les attributs WellFormedProduct (code, product_name...)

        setattr(self, "is_valid", False)  # Définit à l'objet céé l'attribut "is_valid" avec comme valeur "False"

        nbr_of_model_attributs_found_in_downloaded_product = 0
        for field, value in downloaded_product.items():
            if (    value  # Check if the value of the downloaded product is not empty
                    and field in model_attributs):  # Check if all fields (attributs) of the model are in the downloaded product

                nbr_of_model_attributs_found_in_downloaded_product +=1
                # Attribut à l'instance de WellFormedProduct (self) une clef et sa valeur
                setattr(self, field, value)

            if (    nbr_of_model_attributs_found_in_downloaded_product == len(model_attributs)
                    and downloaded_product["lang"] == "fr"):

                setattr(self, "is_valid", True)  # Modifier l'attribut "is_valid" de l'objet créé avec comme nouvelle valeur "True"


def Check_fields_of_product(product_downloaded: dict):
    """Check if all required fields of the product are present.
    Returns an instance. Not a dict!!!"""    
    return WellFormedProduct(product_downloaded)


def get_url(url):
    return requests.get(url).json()


def format_product(product):
    return product


def download_products(required_nbr_of_products: int, keyword):
    
    MAX_WORKERS = 10  # Number of simultaneous requests
    page_nbr = -9
    nbr_of_downloaded_products = 0
    while nbr_of_downloaded_products <= required_nbr_of_products:  # Tant que le nombre de produits voulu n'est pas atteint
        
        page_nbr += MAX_WORKERS
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

        urls = [f"{URL_OPEN_FOOD_FACT}?{params_as_str}{word_to_find_in_product}&page={page_nbr+i}" for i in range(10)]
        nbr_of_empty_response = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            
            list_of_responses = list(pool.map(get_url,urls))

        

        for res in list_of_responses:
            product_not_found = not res.get("products", None)
            if product_not_found:
                nbr_of_empty_response +=1
                continue
            
            for downloaded_product in res['products']:
                
                verified_product = Check_fields_of_product(downloaded_product)
                if not verified_product.is_valid:
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
        
        if nbr_of_empty_response >= MAX_WORKERS:
            
            return