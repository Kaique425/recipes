from django.shortcuts import get_object_or_404, render

from .fake_recipes import make_recipe
from .models import Recipe


def home(request):
    title = "Home"
    recipe = Recipe.objects.filter(is_published=True)
    context = {"recipes": recipe, "title": title}
    return render(request, "recipes/recipe_list.html", context)


def category(request, id):
    recipe = Recipe.objects.filter(category__id=id)
    title = f"{recipe.first().category.name}"
    context = {"recipes": recipe, "title": title}
    return render(request, "recipes/recipe_list.html", context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    title = f"Recipe: {recipe.title}"
    context = {"recipe": recipe, "is_detail_page": True, "title": title}
    return render(request, "recipes/recipe_detail.html", context)
