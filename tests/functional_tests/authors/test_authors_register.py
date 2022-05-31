import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorBaseFunctionalTest


@pytest.mark.functional_test
class AuthorRegisterTest(AuthorBaseFunctionalTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")
        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.ID, "id_email").send_keys("dummy@gmail.com")

        callback(form)

        return form

    def test_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_id("id_first_name", form)
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("Type your first name.", form.text)

        self.form_field_test_with_callback(callback)

    def test_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_id("id_last_name", form)
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("Type your last name.", form.text)

        self.form_field_test_with_callback(callback)

    def test_username_error_messages(self):
        def callback(form):
            username_field = self.get_by_id("id_username", form)
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("This field is required", form.text)

        self.form_field_test_with_callback(callback)

    def test_email_error_messages(self):
        def callback(form):
            username_field = self.get_by_id("id_email", form)
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn("Insert a valid e-mail", form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password = self.get_by_id("id_password", form)
            password2 = self.get_by_id("id_password2", form)
            password.send_keys("PassW@ord123")
            password2.send_keys("PassW@ord321")

            password.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn(
                "Password and password confirmation must be equal",
                form.text,
            )

        self.form_field_test_with_callback(callback)

    def test_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.get_by_id("id_first_name", form).send_keys("First name")
        self.get_by_id("id_last_name", form).send_keys("Last name")
        self.get_by_id("id_username", form).send_keys("my_username")
        self.get_by_id("id_email", form).send_keys("email@gmail.com")
        self.get_by_id("id_password", form).send_keys("PassW@ord123")
        self.get_by_id("id_password2", form).send_keys("PassW@ord123")
        form.submit()
        form = self.get_form()
        self.assertIn(
            "Your account was successfully created as my_username",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
