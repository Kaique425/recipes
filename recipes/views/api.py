from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Recipe


class RecipeApiV2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()
        serializer = RecipeSerializer(instance=recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                author_id=1,
                category_id=1,
                tags=[1, 2],
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class RecipeApiV2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            id=pk,
        )
        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


"""@api_view(("GET", "POST"))
def recipe_api_list(request):
    if request.method == "GET":
        recipes = Recipe.objects.get_published()
        serializer = RecipeSerializer(instance=recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


@api_view(("GET", "PATCH", "DELETE"))
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
    if request.method == "GET":
        serializer = RecipeSerializer(instance=recipe, many=False)

        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )

    elif request.method == "DELETE":
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
