from collections import defaultdict

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

    def validate(self, attrs):
        cd = attrs
        _my_errors = defaultdict(list)

        title = cd.get("title")
        description = cd.get("description")

        if title == description:
            _my_errors["title"].append("Can't be equal to description")
            _my_errors["description"].append("Can't be equal to title")

        if _my_errors:
            raise serializers.ValidationError(_my_errors)

        return super().validate(attrs)

    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError("Title must have at least 5 characters.")

        return title
