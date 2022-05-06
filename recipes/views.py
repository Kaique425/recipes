import os
from urllib import request

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Recipe
from .utils.pagination import make_pagination

PER_PAGE = os.environ.get("PER_PAGE")


def home(request):
    recipes = Recipe.objects.filter(is_published=True)
    title = "Home"
    recipes_paginator = make_pagination(request, recipes, PER_PAGE)
    context = {"recipes": recipes_paginator, "title": title}

    # messages.success(request, "Que legal, Foi com sucesso")

    return render(request, "recipes/recipe_list.html", context)


def category(request, id):
    recipes = Recipe.objects.filter(category__id=id)
    title = f"{recipes.first().category.name}"
    recipes_paginator = make_pagination(request, recipes, PER_PAGE)
    context = {"recipes": recipes_paginator, "title": title}
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
    recipes_paginator = make_pagination(request, recipes, PER_PAGE)
    context = {"search": search, "recipes": recipes_paginator}
    return render(request, "recipes/search.html", context)
