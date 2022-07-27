from collections import defaultdict

from authors.validators import AuthorRecipeValidator
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
            "preparations_time",
            "preparations_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
            "preparation",
            "public",
            "tags",
            "category",
            "author",
        )

    public = serializers.BooleanField(source="is_published", read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)

    def get_preparation(self, recipe):
        return f"{recipe.preparations_time} {recipe.preparations_time_unit}"

    def validate(self, attrs):
        if self.instance is not None and attrs.get("servings") is None:
            attrs["servings"] = self.instance.servings

        if self.instance is not None and attrs.get("preparations_time") is None:
            attrs["preparations_time"] = self.instance.preparations_time

        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super().validate(attrs)
