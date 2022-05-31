import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import create_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = create_browser()
        return super().setUp()

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def tearDown(self):
        self.browser.quit()

        return super().tearDown()
