from django.urls import path

from . import views

app_name = "author"

urlpatterns = [
    path(
        "dashboard/recipe/<int:id>/edit/",
        views.DashboardRecipes.as_view(),
        name="edit_recipe",
    ),
    path("register/", views.register, name="register"),
    path("register/create/", views.register_create, name="create"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("login/validation", views.login_validation_view, name="login-validation"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/recipe/", views.DashboardRecipes.as_view(), name="create_recipe"),
    path(
        "dashboard/delete/<int:id>",
        views.dashboard_recipe_delete,
        name="dashboard_recipe_delete",
    ),
]
