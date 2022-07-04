from django.urls import path

from . import views

app_name = "recipe"
urlpatterns = [
    path("recipes/tags/<slug:slug>/", views.RecipeListViewTag.as_view(), name="tags"),
    path("theory/", views.theory, name="theory"),
    path(
        "api/v1/detail/<int:pk>", views.RecipeDetailViewApi.as_view(), name="api-detail"
    ),
    path("api/v1/home", views.RecipeListViewHomeApi.as_view(), name="api-home"),
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe"),
    path(
        "recipe/category/<int:id>/",
        views.CategoryRecipeListView.as_view(),
        name="category",
    ),
    path("recipe/search/", views.SearchRecipeListView.as_view(), name="search"),
]
