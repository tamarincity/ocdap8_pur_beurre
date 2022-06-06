from django.contrib.auth import get_user_model, login, logout, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect


User = get_user_model()

# Get credentials sent via the form
def _get_credentials(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    return username, password


# Check if the email is properly formed
def check_mail_validity( email: str) -> bool:
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


def login_user(request):
    list(messages.get_messages(request))  # Clear all system messages

    if request.method == 'POST':  # requête via formulaire
        username, password = _get_credentials(request)

        if not username or not password:
            messages.success(request, ("Tous les champs doivent être remplis !"))
            return render(request, 'accounts/signup.html')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('products_home')

        messages.success(request, ("Identifiants incorrects !"))

    return render(request,"accounts/login.html")


def logout_user(request):
    logout(request)
    return redirect('products_home')


def signup_user(request):
    list(messages.get_messages(request))  # Clear all system messages

    if request.method == 'POST':  # requête via formulaire
        username, password = _get_credentials(request)

        if not username or not password:
            messages.success(request, ("Tous les champs doivent être remplis !"))
            return render(request, 'accounts/signup.html')

        is_username_valid = check_mail_validity(username)  # because user email is used as username
        if not is_username_valid:
            messages.success(request, ("Email incorrect !"))
            return render(request, 'accounts/signup.html')

        try:
            # Création de l'utilisateur
            user = User.objects.create_user(username=username, password=password, email=username)

            # Connexion de l'utilisateur
            login(request, user)

            return redirect('products_home')
        
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                messages.success(request, ("Cet utilisateur est déjà enregistré !"))

    return render(request,"accounts/signup.html")


def account(request):
    return render(request,"accounts/account.html")