from django.test.testcases import TestCase
from django.urls import resolve, reverse
from recipes import views

from .factories import RecipeFactory


class RecipeDetailTest(TestCase):
    def test_recipe_detail_page_template_used(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(reverse("recipe:recipe", kwargs={"id": recipe.id}))
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")

    def test_recipe_recipe_detail_status_code(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(reverse("recipe:recipe", kwargs={"id": recipe.id}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_recipe_detail_view_is_correct(self):
        view = resolve(reverse("recipe:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)
