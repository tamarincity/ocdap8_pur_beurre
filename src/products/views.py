import logging

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from products.models import Product, ReceivedMessage
from products import utils


# Create your views here.
def home(request):
    return render(request, 'products/home.html')

def check_email(email):
    if not ("@" in email and "." in email):
        return False
    
    right_part = email.split("@")[1]

    if not "." in right_part:
        return False

    return True


def contact(request):
    return render(request, "products/contact.html")


@login_required
def get_all_favorites(request):
    return render(request, "products/favorites.html")


def get_message(request):

    list(messages.get_messages(request))  # Clear all system messages

    firstname = request.POST.get('firstname', "")
    lastname = request.POST.get('lastname', "")
    email = request.POST.get('email', "")
    phone_number = request.POST.get('phone_number', "")
    message = request.POST.get('message', "")

    context = {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "phone_number": phone_number,
                "message": message,}

    print("email: ", email)

    is_email_well_formed = check_email(email)
    if not is_email_well_formed:
        messages.success(request, ("Le champ email est incorrect !"))
        return render(request, 'products/contact.html', context)

    if not (
            firstname
            and lastname
            and email
            and phone_number
            and message
            and isinstance(firstname, str)
            and isinstance(lastname, str)
            and isinstance(email, str)
            and isinstance(phone_number, str)
            and isinstance(message, str)):

        

        messages.success(request, ("Tous les champs doivent être remplis !"))
        return render(request, 'products/contact.html', context)
    
    try:
        ReceivedMessage.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone_number=phone_number,
            message=message)
        
        messages.success(request, ("Votre message a bien été reçu. Il sera traité dans les plus brefs délais."))
    except Exception as e:
        logging.error(f"Unable to add the customer. Reason: {str(e)}")
        messages.success(request, (
            "Malheureusement, une erreur du système est survenue. Le message n'a pas pu être reçu !"
            " Veuillez ré-essayer plus tard. Merci"))

    return render(request, 'products/message_received.html')


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
        return render(request, 'products/originals.html')

    original_products: list[Product] = None
    if (keywords
            and isinstance(keywords, str)):

        keywords = utils.format_text(keywords)
        original_products = Product.find_original_products(keywords)

    if not original_products:
        logging.info("No original products found!")

    # If there is only one original product found then should redirect to get substitutes
    if original_products and len(original_products) == 1:
        logging.info("Redirect to get_substitutes")
        return redirect(
            reverse('products_get_substitutes')
            + f'?id={original_products[0].id}'
            f'&nutriscore_grade={original_products[0].nutriscore_grade}')

    # Many products found should return the list so the user can choose the good one
    logging.info("Render a list of products found as original products")
    return render(request, "products/originals.html", {"original_products": original_products})


def get_substitutes(request):
    """This route returns a list of substitute products corresponding to the given
    original product ID.
    """

    original_product_id = request.GET.get("id")
    nutriscore_grade = request.GET.get("nutriscore_grade")

    substitute_products = Product.find_substitute_products(
        original_product_id, nutriscore_grade)
    
    original_product = Product.objects.get(id=original_product_id)
    
    return render(request,
        "products/substitutes.html", {
            "substitute_products": substitute_products,
            "original_product": original_product})


def legal_notice(request):
    return render(request, "products/legal_notice.html")


def details(request):
    original_product = Product.objects.get(id=request.GET.get('original_id'))
    substitute_product = Product.objects.get(id=request.GET.get('substitute_id'))

    return render(request, "products/details.html",
        context={'original_product': original_product,
                'substitute_product': substitute_product})
