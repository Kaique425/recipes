from django.shortcuts import render

from .fake_recipes import make_recipe

# Create your views here.


def home(request):
    recipe_list = [make_recipe() for r in range(0, 10)]
    context = {"recipes": recipe_list}
    return render(request, "recipes/recipe_list.html", context)


def recipe(request, id):
    context = {"recipe": make_recipe(), "is_detail_page": True}
    return render(request, "recipes/recipe_detail.html", context)
