from django.contrib.auth import get_user_model
from rest_framework import serializers
from tag.models import Tag

from .models import Category, Recipe

User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "description",
            "is_published",
            "category",
            "author",
            "tags",
            "public",
            "preparation",
        )

    public = serializers.BooleanField(source="is_published", read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)

    def get_preparation(self, recipe):
        return f"{recipe.preparations_time} {recipe.preparations_time_unit}"
