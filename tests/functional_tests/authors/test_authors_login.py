import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorBaseFunctionalTest


@pytest.mark.functional_test
class AuthorLoginTest(AuthorBaseFunctionalTest):
    def test_user_valid_data_can_login_successfully(self):
        password = "testpassword"
        user = User.objects.create_user(username="teste123", password=password)

        self.browser.get(self.live_server_url + reverse("author:login"))
        form = self.get_form()
        username_field = self.get_by_id("id_username", form)
        password_field = self.get_by_id("id_password", form)
        username_field.send_keys(user.username)
        password_field.send_keys(password)
        form.submit()

        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn(f"Your logged as {user.username}", body.text)

    def test_if_login_form_is_invalid(self):
        self.browser.get(self.live_server_url + reverse("author:login"))
        form = self.browser.find_element(
            By.XPATH, "/html/body/main/div[1]/div/div[2]/form"
        )
        form.click()
        username = self.get_by_id("id_username", form)
        password = self.get_by_id("id_password", form)
        username.send_keys(" ")
        password.send_keys(" ")
        form.submit()
        self.assertIn(
            "Invalid form data.", self.browser.find_element(By.TAG_NAME, "body").text
        )

    def test_if_login_credentials_is_invalid(self):
        self.browser.get(self.live_server_url + reverse("author:login"))
        form = self.browser.find_element(
            By.XPATH, "/html/body/main/div[1]/div/div[2]/form"
        )
        form.click()
        username = self.get_by_id("id_username", form)
        password = self.get_by_id("id_password", form)
        username.send_keys("invalid_username")
        password.send_keys("invalid_password")
        form.submit()
        self.assertIn(
            "Invalid password or username.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
