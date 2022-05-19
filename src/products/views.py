import logging

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse

from products.models import Product
from products import utils


# Create your views here.
def index(request):
    return render(request, 'index.html')


def get_origial_product(request):
    try:
        keywords = request.GET['keywords_of_original_product']
    except Exception as e:        
        logging.error('No keywords found for original product')
        return render(request, 'index.html')

    keywords = utils.format_text(keywords)
    original_products = Product.find_original_products(keywords)

    if not original_products:
        logging.info("No original products found!")
    products_as_str = [f"{product.name} - Brands: {product.brands} - Code: {product.code} - Original id:{str(product.original_id)} - Id:{str(product.id)}" for product in original_products]

    # If there is only one original product found then should redirect to get substitutes
    if len(original_products) == 1:
        return redirect(reverse('get_substitutes') + f'?id={original_products[0].id}')

    # Many products found should display the list in order for
    # the user to choose the good one

    return render(request, 'index.html', {"original_products": original_products})


def get_substitutes(request):
    id = request.GET.get("id")
    print("Should return list of substitues")
    return JsonResponse(
        {"substitutes": f"Should return list of substitues for the product with id={id}"})