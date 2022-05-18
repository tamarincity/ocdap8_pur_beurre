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
