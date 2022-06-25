from django.urls import path

from .views import (
    CategoryRecipeListView,
    RecipeDetailView,
    RecipeDetailViewApi,
    RecipeListViewHome,
    RecipeListViewHomeApi,
    SearchRecipeListView,
)

app_name = "recipe"
urlpatterns = [
    path("api/v1/detail/<int:pk>", RecipeDetailViewApi.as_view(), name="api-detail"),
    path("api/v1/home", RecipeListViewHomeApi.as_view(), name="api-home"),
    path("", RecipeListViewHome.as_view(), name="home"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="recipe"),
    path(
        "recipe/category/<int:id>/", CategoryRecipeListView.as_view(), name="category"
    ),
    path("recipe/search/", SearchRecipeListView.as_view(), name="search"),
]
