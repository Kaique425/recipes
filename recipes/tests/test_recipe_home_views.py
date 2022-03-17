from django.test import TestCase
from django.test.testcases import TestCase
from django.urls import resolve, reverse
from recipes import views

from .factories import RecipeFactory


class RecipeHomeTest(TestCase):
    def test_recipe_home_template_used(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(
            reverse("recipe:category", kwargs={"id": recipe.category.id})
        )
        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_recipe_home_view_status_code(self):
        response = self.client.get(reverse("recipe:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse("recipe:home"))
        self.assertIs(view.func, views.home)
