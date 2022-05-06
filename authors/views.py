from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegisterForm

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
        form.save()
        messages.success(request, "Usuário registrado com sucesso.")
        del request.session["register_form"]
    return redirect("author:register")
