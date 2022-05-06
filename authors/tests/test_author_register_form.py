from unittest import TestCase

from authors.forms import RegisterForm
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
    def test_fields_placehoder_is_correct(self, field, placeholder):
        form = RegisterForm()
        field_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(field_placeholder, placeholder)

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
            "password": "Str0ngP@assword1",
            "password2": "Str0ngP@asaword1",
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
