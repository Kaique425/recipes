from unicodedata import category

# from conftest import recipe
from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.tests.factories import CategoryFactory, RecipeFactory


class RecipeSearchTest(TestCase):
    def test_recipe_search_view_is_correct(self):
        view = resolve(reverse("recipe:search")).func
        self.assertIs(view, views.search)

    def test_recipe_search_view_status_code(self):
        status_code = self.client.get(
            reverse("recipe:search") + "?search=Teste"
        ).status_code
        self.assertEqual(status_code, 200)

    def test_recipe_search_template_used(self):
        response = self.client.get(reverse("recipe:search") + "?search=Teste")
        self.assertTemplateUsed(response, "recipes/search.html")

    def test_recipe_search_raises_error_if_any_value_dont_was_passed(self):
        status_code = self.client.get(reverse("recipe:search")).status_code
        self.assertEqual(status_code, 404)

    def test_recipe_search_by_title(self):
        recipe = RecipeFactory(title="recipe one", is_published=True)

        search_url = reverse("recipe:search")
        response = self.client.get(f"{search_url}?search={recipe.title}")

        self.assertIn(recipe.title, response.context["recipes"][0].title)
