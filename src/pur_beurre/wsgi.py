"""
WSGI config for pur_beurre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pur_beurre.settings')

application = get_wsgi_application()

# =================================================================
# Automatically creating super user
from django.contrib.auth.models import User

import environ

env = environ.Env(DEBUG=(bool, False))

users = User.objects.all()

if not users:
    User.objects.create_superuser(
        username=env('DJANGO_SUPERUSER_USERNAME'),
        email=env('DJANGO_SUPERUSER_EMAIL'),
        password=env('DJANGO_SUPERUSER_PASSWORD'),
        is_active=True,
        is_staff=True)
