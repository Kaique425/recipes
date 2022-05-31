from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm

# Create your views here.


def register(request):
    data = request.session.get("register_form", None)
    form = RegisterForm(data)
    return render(request, "authors/pages/register.html", context={"form": form})


@require_POST
def register_create(request):
    POST = request.POST
    request.session["register_form"] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user: object = form.save(commit=False)
        user.set_password(user.password)
        messages.success(
            request, f"Your account was successfully created as {user.username}"
        )
        user.save()
        del request.session["register_form"]
        return redirect(reverse("author:login"))
    else:
        print("Invalido")
    return redirect("author:register")


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("recipe:home"))
    form = LoginForm()
    context = {"form": form}
    return render(request, "authors/pages/login.html", context)


@require_POST
@login_required(login_url="author:login", redirect_field_name="next")
def logout_view(request):
    if request.POST.get("username") != request.user.username:
        return redirect(reverse("author:login"))
    logout(request)
    return redirect(reverse("author:login"))


@require_POST
def login_validation_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        authenticated_user = authenticate(
            username=username,
            password=form.cleaned_data.get("password"),
        )
        if authenticated_user is not None:
            messages.success(request, f"Your logged as {username}")
            login(request, authenticated_user)

        else:
            messages.error(request, "Invalid password or username.")
    else:
        messages.error(request, "Invalid form data.")
    return redirect(reverse("author:login"))
