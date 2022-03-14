from unicodedata import category

from conftest import recipe
from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.tests.factories import CategoryFactory, RecipeFactory


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

    def test_recipe_search_view_is_correct(self):
        view = resolve(reverse("recipe:search")).func
        self.assertIs(view, views.search)

    def test_recipe_home_view_status_code(self):
        response = self.client.get(reverse("recipe:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_recipe_detail_status_code(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(reverse("recipe:recipe", kwargs={"id": recipe.id}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_status_code(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(
            reverse("recipe:category", kwargs={"id": recipe.category.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_search_view_status_code(self):
        status_code = self.client.get(
            reverse("recipe:search") + "?search=Teste"
        ).status_code
        self.assertEqual(status_code, 200)

    def test_recipe_home_template_used(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(
            reverse("recipe:category", kwargs={"id": recipe.category.id})
        )
        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_recipe_detail_page_template_used(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(reverse("recipe:recipe", kwargs={"id": recipe.id}))
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")

    def test_recipe_category_template_used(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(
            reverse("recipe:category", kwargs={"id": recipe.category.id})
        )

        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_recipe_search_template_used(self):
        response = self.client.get(reverse("recipe:search") + "?search=Teste")
        self.assertTemplateUsed(response, "recipes/search.html")

    def test_recipes_search_raises_error_if_any_value_dont_was_passed(self):
        status_code = self.client.get(reverse("recipe:search")).status_code
        self.assertEqual(status_code, 404)

    def test_if_recipe_search_is_escaped(self):
        url = reverse("recipe:search") + "?search=Teste"
        response = self.client.get(url)
        self.assertIn(f"Teste", response.content.decode("utf-8"))
