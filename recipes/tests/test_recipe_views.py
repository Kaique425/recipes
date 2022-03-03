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
