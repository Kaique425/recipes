import factory
import pytest
from django.contrib.auth.models import User
from factory import fuzzy
from faker import Faker
from recipes.models import Category, Recipe

pytestmark = pytest.mark.django_db

Faker.seed(0)
faker = Faker(["pt_BR"])


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = faker.first_name()
    last_name = faker.last_name()
    username = faker.user_name()
    password = faker.password(length=12)
    email = faker.email()


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    title = fuzzy.FuzzyText()
    description = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    slug = faker.slug()
    preparations_time = fuzzy.FuzzyInteger(5.0, 999)
    preparations_time_unit = "Minutes"
    servings = fuzzy.FuzzyInteger(5.0, 999)
    servings_unit = "Person"
    preparation_steps = factory.Faker(
        "paragraph", nb_sentences=5, variable_nb_sentences=True
    )
    praparation_steps_is_html = False
    created_at = faker.date()
    updated_at = faker.date()
    is_published = factory.Faker("pybool")
    cover = factory.django.ImageField()
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(AuthorFactory)


def make_recipes(qtd=1):
    author_teste = AuthorFactory()
    if qtd == 1:
        return RecipeFactory()
    recipes = [
        RecipeFactory(is_published=True, author=author_teste) for r in range(0, qtd)
    ]
    return recipes
