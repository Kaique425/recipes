from urllib import request

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

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


def search(request: request):
    search = request.GET.get("search", "").strip()
    if not search:
        raise Http404()
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search) | Q(description__icontains=search),
            is_published=True,
        )
    ).order_by("-id")
    context = {"search": search, "recipes": recipes}
    return render(request, "recipes/search.html", context)
