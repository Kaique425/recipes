import pytest
from conftest import recipe
from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from parameterized import parameterized

from .factories import CategoryFactory, RecipeFactory

pytestmark = pytest.mark.django_db


class RecipeModelTest(TestCase):
    def test_recipe_title_str(self):
        recipe = RecipeFactory(is_published=True)
        self.assertEqual(recipe.title, recipe.__str__())

    def test_if_recipe_str_is_equal_title(self):
        recipe = RecipeFactory(is_published=True)
        self.assertEqual(recipe.__str__(), recipe.title)

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparations_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        recipe = RecipeFactory(is_published=True)
        setattr(recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_if_preparation_steps_is_html_is_false(self):
        recipe = RecipeFactory()

        self.assertFalse(
            recipe.praparation_steps_is_html,
            msg="Preparation_steps_is_html is not False by default.",
        )


class CategoryTest(TestCase):
    def test_category_name_str(self):
        category = CategoryFactory()

        self.assertEqual(category.name, category.__str__())
