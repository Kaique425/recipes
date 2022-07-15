from django.urls import path

from .views import api, site

app_name = "recipe"
urlpatterns = [
    path("recipes/tags/<slug:slug>/", site.RecipeListViewTag.as_view(), name="tags"),
    path("theory/", site.theory, name="theory"),
    path("", site.RecipeListViewHome.as_view(), name="home"),
    path("recipe/<int:pk>/", site.RecipeDetailView.as_view(), name="recipe"),
    path(
        "recipe/category/<int:id>/",
        site.CategoryRecipeListView.as_view(),
        name="category",
    ),
    path("recipe/search/", site.SearchRecipeListView.as_view(), name="search"),
    path(
        "api/v1/detail/<int:pk>", site.RecipeDetailViewApi.as_view(), name="api-detail"
    ),
    path("api/v1/home", site.RecipeListViewHomeApi.as_view(), name="api-home"),
    path("recipe/api/v2/list", api.recipe_api_list, name="api-recipe-list"),
    path("recipe/api/v2/<int:pk>", api.recipe_api_detail, name="api-recipe-detail"),
]
