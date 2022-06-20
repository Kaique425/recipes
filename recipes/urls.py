from django.urls import path

from .views import (
    CategoryRecipeListView,
    RecipeDetailView,
    RecipeListViewHome,
    SearchRecipeListView,
)

app_name = "recipe"
urlpatterns = [
    path("", RecipeListViewHome.as_view(), name="home"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="recipe"),
    path(
        "recipe/category/<int:id>/", CategoryRecipeListView.as_view(), name="category"
    ),
    path("recipe/search/", SearchRecipeListView.as_view(), name="search"),
]
