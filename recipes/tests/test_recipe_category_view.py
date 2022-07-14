from django.test import TestCase
from django.urls import resolve, reverse
from recipes.views import site

from .factories import RecipeFactory


class RecipeCategoryTest(TestCase):
    def test_recipe_category_view_status_code(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(
            reverse("recipe:category", kwargs={"id": recipe.category.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_template_used(self):
        recipe = RecipeFactory(is_published=True)
        response = self.client.get(
            reverse("recipe:category", kwargs={"id": recipe.category.id})
        )

        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse("recipe:category", kwargs={"id": 1}))
        self.assertIs(view.func.view_class, site.CategoryRecipeListView)
