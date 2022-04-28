import logging

import requests
from icecream import ic

from products.constants import (
    NBR_OF_PAGES,
    URL_OPEN_FOOD_FACT,
    REQUIRED_FIELDS_OF_A_PRODUCT,
)


def request_get(URL_OPEN_FOOD_FACT, params):

    try:
        ic("Downloading ...")
        response =  requests.get(URL_OPEN_FOOD_FACT, params=params).json()
        return response.get('products')

    except Exception as e:
        ic(str(e))
        logging.error(str(e))
        return None


def download_data(quantity_of_products, keyword):
    """Get data from Open Food Fact API"""
    ic()

    page_nbr = 0
    rough_products = []
    products_per_page = quantity_of_products // NBR_OF_PAGES

    params = {
            "action": "process",
            "sort_by": "unique_scan_n",
            "search_terms": "boissons",
            "fields": REQUIRED_FIELDS_OF_A_PRODUCT,
            "page_size": f"{products_per_page}",
            "json": "1"}
    
    if keyword not in ["any", "all"]:
        params["tagtype_0"] = "categories"
        params["tag_contains_0"] = "contains"
        params["tag_0"] = keyword

    for i in range(NBR_OF_PAGES):
        page_nbr += 1
        params["page"] = page_nbr

        rough_products += request_get(URL_OPEN_FOOD_FACT, params)
        if not rough_products:
            break

    return rough_products
