from django.urls import path

from .views import home, recipe

app_name = "recipe"
urlpatterns = [
    path("", home, name="home"),
    path("recipes/<int:id>", recipe, name="recipe"),
]
