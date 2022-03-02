from django.urls import path

from .views import category, home, recipe

app_name = "recipe"
urlpatterns = [
    path("", home, name="home"),
    path("recipe/<int:id>/", recipe, name="recipe"),
    path("recipe/category/<int:id>/", category, name="category"),
]
