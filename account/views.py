from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.forms import SignUpForm
from account.models import Account
from django.contrib import messages, auth
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data["first_name"]
            lastname = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            Account.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password)
            messages.add_message(request, messages.SUCCESS, "Registered Successfully")
            return redirect("signin")
    else:
        form = SignUpForm()

    context = {"hide_header": True, "form": form}
    return render(request, "account/signup.html", context=context)

def signin(request):
    next_url = request.GET.get("next")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        next_url = request.POST["next"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=settings.ALLOWED_HOSTS):
                return redirect(next_url)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("signin")

    context = {"hide_header": True, "next_url": next_url}
    return render(request, "account/signin.html", context=context)

@login_required
def sign_out(request):
    auth.logout(request)
    messages.success(request, "Logged Out")
    return redirect("homepage")
