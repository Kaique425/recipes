from django.contrib.auth import get_user_model
from rest_framework import serializers
from tag.models import Tag

from .models import Category

User = get_user_model()


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source="is_published")
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    def get_preparation(self, recipe):
        return f"{recipe.preparations_time} {recipe.preparations_time_unit}"
