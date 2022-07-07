from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag

from .models import Category, Recipe

"""class TagInline(GenericStackedInline):
    model = Tag
    fields = ("name",)
    extra = 1

"""


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "is_published")
    list_disnamplay_links = "title", "created_at"
    search_fields = "id", "title", "description"
    list_editable = ("is_published",)
    list_filter = ("is_published", "category", "author")
    list_per_page = 12
    ordering = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}

    autocomplete_fields = ("tags",)


"""    inlines = [
        TagInline,
    ]
"""
