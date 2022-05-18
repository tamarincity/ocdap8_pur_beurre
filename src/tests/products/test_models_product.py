import pytest

from products.models import Product

pytestmark = pytest.mark.django_db  # Create a virtual database

class TestProductModel:

    def add_a_product(self):
        return Product.objects.create(
            image_thumb_url="url-thumb-image",
            image_url="url-thumb-image",
            ingredients_text="list of ingredients",
            keywords="some keywords (mega key_words)",
            name="Product name",
            nutriments="Some nutriments",
            nutriscore_grade="Grade (A B C D E)",
            original_id=9876543210,
            quantity="Quantity",
            stores="All the stores where you can find the product",
            url="url_of_the_website_of_the_product",
        )

    def test_should_add_a_product_to_the_db(self):
        product = self.add_a_product()

        assert product.image_thumb_url == "url-thumb-image"
        assert product.image_url == "url-thumb-image"
        assert product.ingredients_text == "list of ingredients"
        assert product.keywords == "some keywords (mega key_words)"
        assert product.name == "Product name"
        assert product.nutriments == "Some nutriments"
        assert product.nutriscore_grade == "Grade (A B C D E)"
        assert product.original_id == 9876543210
        assert product.quantity == "Quantity"
        assert product.stores == "All the stores where you can find the product"
        assert product.url == "url_of_the_website_of_the_product"

        assert Product.objects.all().count() == 1


    def test_should_not_be_able_to_add_the_same_product_to_the_db(self):
        expected = "unique original_id violation"
        result = "Test failed"

        self.add_a_product()
        try:
            self.add_a_product()
        except Exception as e:

            if "unique" in str(e).lower():
                result = expected
        
        assert result == expected
