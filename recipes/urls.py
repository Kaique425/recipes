from django.urls import path

from .views import category, home, recipe

app_name = "recipe"
urlpatterns = [
    path("", home, name="home"),
    path("recipes/<int:id>", recipe, name="recipes"),
    path("recipes/category/<int:category_id>", category, name="category"),
]
