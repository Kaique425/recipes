import re

from attr import fields
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")
    if not regex.match(password):
        raise ValidationError(
            ("Weak password..."),
            code="invalid",
        )

    return password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Ex John"
        self.fields["last_name"].widget.attrs["placeholder"] = "Ex Doe"
        self.fields["email"].widget.attrs["placeholder"] = "Type your e-mail"

    first_name = forms.CharField(
        required=True,
        label="First name",
        error_messages={"required": "Type your first name."},
    )

    last_name = forms.CharField(
        required=True,
        label="Last name",
        error_messages={"required": "Type your last name."},
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat your password here."}),
        error_messages={
            "required": "Please, repeat your password",
        },
        label="Password Confirmation",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Type your password here."},
        ),
        error_messages={"required": "Password must not be empty"},
        help_text=(
            "Password must have at least one uppercase letter,"
            "one lowercase letter and one number. The length should be"
            "at least 8 characters."
        ),
        validators=[
            strong_password,
        ],
        label="Password",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

        help_texts = {
            "email": "Insert a valid e-mail",
        }

        error_messages = {
            "username": {
                "required": "This field is required",
                "valid": "Type a valid username",
            },
        }
        labels = {
            "email": "E-mail",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Type your username"},
            ),
        }

    def clean_first_name(self):
        data = self.cleaned_data.get("first_name")

        if "teste" in data:
            raise ValidationError(
                "Don't type %(value)s as your first name.",
                code="invalid",
                params={"value": '"Jon Doe"'},
            )
        return data

    def clean_password(self):
        data = self.cleaned_data.get("password")

        if "atenção" in data:
            raise ValidationError(
                "Don't type %(value)s as your password",
                code="invalid",
                params={"value": '"atenção"'},
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError(
                {
                    "password": "Passwords must be equals",
                    "password2": ValidationError(
                        "Passwords must be equals",
                        code="invalid",
                    ),
                }
            )
