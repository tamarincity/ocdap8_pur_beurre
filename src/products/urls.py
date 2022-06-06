from django.urls import path

from products import views

urlpatterns = [
    # Home page
    path('home', views.home, name='products_home'),
    # Route to get the original product after submitting the form
    path('favorites', views.get_all_favorites, name='products_favorites'),
    # Route to get the original product after submitting the form
    path('contact', views.contact, name='products_contact'),
    # Route to get the original product after submitting the form
    path('get-origial-product', views.get_origial_product, name='products_get_origial_product'),
    # Route to get a list of substitute products for an original product
    path('get-substitutes', views.get_substitutes, name='products_get_substitutes'),
    # Route to get a list of substitute products for an original product
    path('legal_notice', views.legal_notice, name='products_legal_notice'),
    # Home page
    path('', views.home, name='products_home'),
]
