import pytest

from recipes.tests.factories import RecipeFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def recipe():
    return RecipeFactory()
