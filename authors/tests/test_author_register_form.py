from unittest import TestCase

from authors.forms.register_form import RegisterForm
from django.shortcuts import reverse
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("first_name", "Ex John"),
            ("last_name", "Ex Doe"),
            ("email", "Type your e-mail"),
            ("username", "Type your username"),
            ("password", "Type your password here."),
            ("password2", "Repeat your password here."),
        ]
    )
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            ("email", "Insert a valid e-mail"),
            (
                "password",
                "Password must have at least one uppercase letter,"
                "one lowercase letter and one number. The length should be"
                "at least 8 characters.",
            ),
        ]
    )
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(current_help_text, help_text)

    @parameterized.expand(
        [
            ("first_name", "First name"),
            ("last_name", "Last name"),
            ("email", "E-mail"),
            ("username", "Username"),
            ("password", "Password"),
            ("password2", "Password Confirmation"),
        ]
    )
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anyemail.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword1",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand(
        [
            ("username", "This field is required"),
            ("first_name", "Type your first name."),
            ("last_name", "Type your last name."),
            ("password", "Password must not be empty"),
            ("password2", "Please, repeat your password"),
        ],
    )
    def test_field_can_not_be_empty(self, field, message):
        self.form_data[field] = ""
        url = reverse("author:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.context["form"].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data["username"] = "Jo"
        url = reverse("author:create")
        message = "Ensure this value has at least 4 characters."
        response = self.client.post(url, data=self.form_data, follow=True)
        ...
        self.assertIn(message, response.context["form"].errors.get("username"))

    def test_usename_field_max_length_should_be_150(self):
        self.form_data["username"] = "a" * 151
        url = reverse("author:create")
        message = "Username must have less than 150 characters."
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.context["form"].errors.get("username"))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data["password"] = "@Abc1234"
        self.form_data["password2"] = "@Abc123"

        url = reverse("author:create")
        msg = "Password and password confirmation must be equal"
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context["form"].errors.get("password"))

    def test_raise_validation_error_if_password_is_weak(self):
        self.form_data["password"] = "teste"
        self.form_data["password2"] = "teste"
        url = reverse("author:create")
        msg = "Weak password..."
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context["form"].errors.get("password"))

    def test_raise_email_validation_error_if_is_already_in_use(self):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anyemail.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword1",
        }
        url = reverse("author:create")
        response_creation = self.client.post(url, data=self.form_data, follow=True)

        self.form_data["email"] = "email@anyemail.com"

        url2 = reverse("author:create")
        msg = "User e-mail already in use."
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context["form"].errors.get("email"))

    def teste_creation(self):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anyemail.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword1",
        }
        url = reverse("author:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        code = response.status_code
        self.assertEqual(code, 200)

    """def test_author_created_can_login(self):
        url = reverse("author:create")

        self.form_data.update(
            {
                "username": "testuser",
                "password": "@Bc123456",
                "password2": "@Bc123456",
            }
        )

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(username="testuser", password="@Bc123456")

        self.assertTrue(is_authenticated)"""
