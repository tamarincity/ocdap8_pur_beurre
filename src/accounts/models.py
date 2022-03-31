from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class UserRole(models.TextChoices):
        CUSTOMER = "Client"
        PREMIUM_CUSTOMER = "Client Premium"
        VIP = "VIP"

    user_role = models.CharField(
        choices=UserRole.choices, default=UserRole.CUSTOMER, max_length=30
    )
