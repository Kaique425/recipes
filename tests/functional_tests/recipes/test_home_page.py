import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest

from recipes.tests.factories import RecipeFactory, make_recipes


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_home_page_without_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("Não há receitas pra serem exibidas.", body.text)

    def test_recipe_search_can_find_correct_recipe(self):
        self.browser.get(self.live_server_url)
        recipe = RecipeFactory(is_published=True)
        search = self.browser.find_element(
            By.XPATH, "//input[@placeholder='Search for a recipe']"
        )
        title = recipe.title
        search.send_keys(title)
        search.send_keys(Keys.ENTER)
        self.assertIn(title, self.browser.find_element(By.TAG_NAME, "body").text)

    def test_recipe_home_page_pagination(self):
        recipes = make_recipes(6)
        self.browser.get(self.live_server_url)
        index = self.browser.find_element(By.XPATH, "/html/body/main/div[2]/a[3]")
        index.click()
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, "card")), 3)
