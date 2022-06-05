from django.shortcuts import render


def login_user(request):
    return render(request,"accounts/login.html")


def logout_user(request):
    return render(request,"accounts/logout.html")


def signup_user(request):
    print()
    print("DANS LA VIEW SIGNUP !")
    print()
    return render(request,"accounts/signup.html")

def account(request):
    return render(request,"accounts/account.html")