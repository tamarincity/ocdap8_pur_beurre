from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Customer(AbstractUser):
    class CustomerType(models.TextChoices):
        CUSTOMER = "Client"
        PREMIUM_CUSTOMER = "Client Premium"
        VIP = "VIP"

    customer_type = models.CharField(
        choices=CustomerType.choices, default=CustomerType.CUSTOMER, max_length=30
    )


class Product (models.Model):
   name = models.CharField(max_length=50, help_text='Name of the product')
   off_id = models.IntegerField()
   quantity = models.CharField(max_length=20)
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
   nutriments_100g = models.TextField()


   #Metadata
   class Meta :
       ordering = ['name']

   #Methods
   def __str__(self):
       return self.name


class L_Favorite (models.Model):
   customer = models.ForeignKey('Customer', related_name='favorites', on_delete=models.CASCADE)
   original_product = models.ForeignKey('Product', related_name="original_products", on_delete=models.CASCADE)
   substitue_product = models.ForeignKey('Product', related_name="substite_products", on_delete=models.CASCADE)

   #Methods
   def __str__(self):
        return f"{self.original_product}/{self.substitue_product} ({self.customer})"


class Category(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('Product', related_name='categories')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
