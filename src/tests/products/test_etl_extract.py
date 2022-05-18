import pytest
import requests

from src.products import etl_extract
from src.products.etl_extract import (
    Check_fields_of_product,
    download_products,
    get_url,
    WellFormedProduct,
)

from products.constants import (
    ETL_EXTRACT_MAX_WORKERS,
    URL_OPEN_FOOD_FACT,
)

from params_for_mark_parametrize.params_etl_extract import (
    good_downloaded_product,
    downloaded_product_with_a_missing_field,
    downloaded_product_with_an_empty_value
)

@pytest.mark.parametrize(
    "arg_explanation, what_should_happen, downloaded_product, expected_value",
    [   (   "Well formed downloading product",
            "Should return a instance of WellFormedProduct with the 'is_valid' property = True",
            good_downloaded_product,            
            True),
        (   "Downloaded product with a missing required field",
            "Should return a instance of WellFormedProduct with the 'is_valid' property = False",
            downloaded_product_with_a_missing_field,
            False),
        (   "Downloaded product with a required field that is existing but empty",
            "Should return a instance of WellFormedProduct with the 'is_valid' property = False",
            downloaded_product_with_an_empty_value,
            False),
        (   "None as downloaded product",
            "Should return False",
            None,
            False),
        (   "product_downloaded is not a dict",
            "Should return False",
            ["not", "a", "dict"],
            False),
            ])
def test_Check_fields_of_product(
        arg_explanation,
        what_should_happen,
        downloaded_product,
        expected_value):
    
    
    print(arg_explanation, " ", what_should_happen)
    product = Check_fields_of_product(downloaded_product)
    if (    downloaded_product
            and isinstance(downloaded_product, dict)):

        assert isinstance(product, WellFormedProduct)
        assert product.is_valid == expected_value
    else:
        assert product == expected_value

@pytest.mark.test_me
def test_get_url():
    print("url is empty should raise exception: requests.exceptions.MissingSchema")
    with pytest.raises(requests.exceptions.MissingSchema):
        get_url("")

    print("url is not a string should raise exception: requests.exceptions.MissingSchema")
    with pytest.raises(requests.exceptions.MissingSchema):
        get_url({"message", "not a string"})

    print("Wrong endpoint should raise exception: requests.exceptions.JSONDecodeError")
    with pytest.raises(requests.exceptions.JSONDecodeError):
        get_url("https://fr.openfoodfacts.org/cgi/search.pl")

    print("Correct url should return json of products")
    assert "products" in get_url(
        "https://fr.openfoodfacts.org/cgi/search.pl"
        "?action=process&sort_by=unique_scan_n&page_size=5&json=1")


class TestDownloadProducts():

    is_first_page_in_first_group_of_request = False
    is_any_page_of_second_group_of_request = False

    def test_download_products(self, monkeypatch):
        required_nbr_of_products = 15

        
        
        def mock_get_url(url):
            
            if URL_OPEN_FOOD_FACT in url and "&page=1" in url:
                self.is_first_page_in_first_group_of_request = True
            if URL_OPEN_FOOD_FACT in url and f"&page={ETL_EXTRACT_MAX_WORKERS + 1}" in url:
                self.is_any_page_of_second_group_of_request = True
            if (    self.is_first_page_in_first_group_of_request == True
                    and self.is_first_page_in_first_group_of_request == True):

                return {"products": [good_downloaded_product, downloaded_product_with_an_empty_value]}

        monkeypatch.setattr(etl_extract, "get_url", mock_get_url)
        assert (
            len(list(download_products(required_nbr_of_products, "a keyword"))) == 
                TODO dautres mocks)
