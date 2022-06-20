from django.contrib import admin

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "is_published")
    list_display_links = "title", "created_at"
    search_fields = "id", "title", "description"
    list_editable = ("is_published",)
    list_filter = ("is_published", "category", "author")
    list_per_page = 12
    ordering = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
