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
    """Beforehand, the user has entered keywords to find the original product he
    wants to replace.
    Through this route, we try to find the original product.
    If only one product is found, the user is redirected to the list of matching
    substitute products.
    Otherwise, we return a list of original products that match the keywords. This
    way, the user can choose the right original product.
    """
    try:
        keywords = request.GET['keywords_of_original_product']
    except Exception as e:        
        logging.error('No keywords found for original product')
        return render(request, 'index.html')

    keywords = utils.format_text(keywords)
    original_products = Product.find_original_products(keywords)

    if not original_products:
        logging.info("No original products found!")

    # If there is only one original product found then should redirect to get substitutes
    if len(original_products) == 1:
        return redirect(
            reverse('get_substitutes')
            + f'?id={original_products[0].id}'
            f'&nutriscore_grade={original_products[0].nutriscore_grade}')

    # Many products found should return the list so the user can choose the good one
    return render(request, "index.html", {"original_products": original_products})


def get_substitutes(request):
    """This route returns a list of substitute products corresponding to the given
    original product ID.
    """
    id = request.GET.get("id")
    nutriscore_grade = request.GET.get("nutriscore_grade")

    substitute_products = Product.find_substitute_products(
        id, nutriscore_grade)
    return render(request,
        "substitutes.html", {"substitute_products": substitute_products})