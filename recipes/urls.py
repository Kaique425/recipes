from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import api, site

recipe_api_router = SimpleRouter()
recipe_api_router.register(
    "recipe/api/v2",
    api.RecipeV2ViewSet,
)

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
    path("", include(recipe_api_router.urls)),
]

"""path(
    "recipe/api/v2/list",
    api.RecipeV2ViewSet.as_view(
        {
            "get": "list",
            "post": "create",
        }
    ),
    name="api-recipe-list",
),
path(
    "recipe/api/v2/<int:pk>",
    api.RecipeV2ViewSet.as_view(
        {
            "get": "retrieve",
            "post": "partial_update",
        }
    ),
    name="api-recipe-detail",
),""",
