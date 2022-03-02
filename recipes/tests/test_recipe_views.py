from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse("recipe:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse("recipe:category", kwargs={"id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_recipe_detail_view_is_correct(self):
        view = resolve(reverse("recipe:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)
