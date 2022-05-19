from django.urls import path

from products import views

urlpatterns = [
    path('', views.index, name='index'),
    # Route to get the original product after submitting the form
    path('get-origial-product', views.get_origial_product, name='get_origial_product'),
    # Route to get a list of substitute products for an original product
    path('get-substitutes', views.get_substitutes, name='get_substitutes'),
]