import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import create_browser


class AuthorBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = create_browser()

        return super().setUp()

    def tearDown(self):
        self.browser.close()

        return super().tearDown()

    def sleep(self, qtd=5):
        time.sleep(qtd)

    def get_form(self):
        FORM_XPATH = "/html/body/main/div/div/div[2]/form"
        form = self.browser.find_element(By.XPATH, FORM_XPATH)
        return form

    def get_by_id(self, id, html_element):
        element = html_element.find_element(By.ID, id)
        return element
