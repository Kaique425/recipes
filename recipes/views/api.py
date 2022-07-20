from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Recipe


@api_view(("GET", "POST"))
def recipe_api_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.get_published()
        serializer = RecipeSerializer(instance=recipes, many=True)

    elif request.method == "POST":
        print(f"data: {request.data}")
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                author_id=1,
                category_id=1,
                tags=[1, 2],
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(("GET",))
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    serializer = RecipeSerializer(instance=recipe, many=False)

    return Response(serializer.data)
