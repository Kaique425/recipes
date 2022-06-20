from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from recipes.forms import RecipeForm
from recipes.models import Recipe

from .forms import LoginForm, RegisterForm


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
@login_required(login_url="author:login")
def logout_view(request):
    if request.POST.get("username") != request.user.username:
        messages.error(request, "Invalid user logout")
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


@login_required(login_url="author:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user)

    context = {"recipes": recipes}
    return render(request, "authors/pages/dashboard.html", context)


@login_required(login_url="author:login", redirect_field_name="next")
def create_recipe_view(request):
    form = RecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, "Recipe created successfully.")
        return redirect(reverse("author:dashboard"))
    context = {"form": form}
    return render(request, "authors/pages/create_recipe.html", context)


@require_POST
@login_required(login_url="author:login", redirect_field_name="next")
def dashboard_recipe_delete(request, id):
    recipe: object = Recipe.objects.get(pk=id)
    recipe.delete()
    messages.success(request, "Deleted successfully.")
    return redirect(reverse("author:dashboard"))


@method_decorator(
    login_required(login_url="author:login", redirect_field_name="next"),
    name="dispatch",
)
class DashboardRecipes(View):
    def return_render(self, recipe, form):
        context = {"form": form, "recipe": recipe}
        return render(self.request, "authors/pages/edit_recipe.html", context)

    def get_recipe(self, id):
        recipe = None
        if id:
            recipe = Recipe.objects.filter(
                is_published=False, author=self.request.user, pk=id
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = RecipeForm(
            instance=recipe,
        )

        return self.return_render(recipe, form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = RecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )
        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.praparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, "Your recipe was edited successfully")
            return redirect(reverse("author:edit_recipe", args=(recipe.id,)))

        return self.return_render(recipe, form)
