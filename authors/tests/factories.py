import factory
import pytest
from django.contrib.auth.models import User
from factory import fuzzy
from faker import Faker
from recipes.models import Category, Recipe

pytestmark = pytest.mark.django_db

Faker.seed(0)
faker = Faker(["pt_BR"])


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = faker.first_name()
    last_name = faker.last_name()
    username = faker.user_name()
    password = faker.password(length=12)
    email = faker.email()
