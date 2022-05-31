from django.urls import path

from . import views

app_name = "author"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/create/", views.register_create, name="create"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("login/validation", views.login_validation_view, name="login-validation"),
]
