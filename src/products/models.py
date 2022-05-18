import logging

from django.db import models
from django.db import transaction

from accounts.models import Customer

from .constants import PRODUCT_NAME_MAX_LENGTH, QUANTITY_MAX_LENGTH


# Create your models here.

class Product (models.Model):
    name = models.CharField(max_length=PRODUCT_NAME_MAX_LENGTH, help_text='Name of the product')
    original_id = models.BigIntegerField(unique=True, db_index=True)
    quantity = models.CharField(max_length=QUANTITY_MAX_LENGTH)
    # keywords = (str(_keywords) + categories + product_name + generic_name + code)
    keywords = models.TextField()
    url = models.URLField()
    image_url = models.URLField()
    image_thumb_url = models.URLField()
    nutriscore_grade = models.CharField(max_length=2)
    ingredients_text = models.TextField()
    stores = models.TextField()
    # nutriments_100g = these to string =>(
    # nutriments["energy-kcal"], nut..["fat_100g"], ["fat_unit"], ["fiber_100g"], ["fiber_unit"],
    # ["proteins_100g"], ["proteins_unit"], ["salt_100g"], ["salt_unit"], ["sugar_100g"], ["sugar_unit"])
    nutriments = models.JSONField()


    #Metadata
    class Meta :
        ordering = ['name']

    #Methods
    def __str__(self):
        return self.name

    @classmethod
    def add_many(cls, products: list, stored_categories: dict)->bool:
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
                            raise Exception(str(e))

                    for category in product.categories:
                        stored_category = Category.objects.get(name=category)
                        stored_category.products.add(stored_product)

            if not is_new_product_added:
                print("No new product added to the database!")
            return True
        except Exception as e:
            logging.error("Error adding products. Exception was: %s", e)
            return False


class L_Favorite (models.Model):
    customer = models.ForeignKey(Customer, related_name='favorites', on_delete=models.CASCADE)
    original_product = models.ForeignKey('Product', related_name="original_products", on_delete=models.CASCADE)
    substitue_product = models.ForeignKey('Product', related_name="substite_products", on_delete=models.CASCADE)

    #Methods
    def __str__(self):
        return f"{self.original_product}/{self.substitue_product} ({self.customer})"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('Product', related_name='categories')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def add_many(cls, categories: list)->dict:
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
                        stored_categories[category] = Category.objects.get_or_create(name=category)
                    except Exception as e:
                        raise Exception(str(e))

            return stored_categories
        except Exception as e:
            logging.error("Error adding categories. Exception was: %s", e)
