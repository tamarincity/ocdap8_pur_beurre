import copy

from src.products.utils import (
    WellFormedProduct)
from params_for_mark_parametrize.params_etl_extract import (good_downloaded_product)


good_downloaded_product_obj = WellFormedProduct(good_downloaded_product)

dl_product1 = copy.deepcopy(good_downloaded_product_obj)
dl_product1.code = 1012345678111
dl_product1._id = 1000000001
dl_product1.categories = ["cat1", "cat2", "cat3"]

dl_product2 = copy.deepcopy(good_downloaded_product_obj)
dl_product2.code = 2012345678222
dl_product1._id = 2000000002
dl_product1.categories = ["cat3", "cat4", "cat5"]