from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.form_funcs import strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Ex John"
        self.fields["last_name"].widget.attrs["placeholder"] = "Ex Doe"
        self.fields["email"].widget.attrs["placeholder"] = "Type your e-mail"
        self.fields["username"].widget.attrs["placeholder"] = "Type your username"

    username = forms.CharField(
        label="Username",
        help_text=(
            "Username must have letters, numbers or one of those @.+-_.",
            "The lengh should be between 4 and 150 characters.",
        ),
        error_messages={
            "required": "This field is required",
            "min_length": "Ensure this value has at least 4 characters.",
            "max_length": "Username must have less than 150 characters.",
        },
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        label="First name",
        error_messages={"required": "Type your first name."},
    )

    last_name = forms.CharField(
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

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        author = User.objects.filter(email=email).exists()
        if author:
            raise ValidationError("User e-mail already in use.", code="invalid")
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            password_confirmation_error = ValidationError(
                "Password and password confirmation must be equal", code="invalid"
            )
            raise ValidationError(
                {
                    "password": password_confirmation_error,
                    "password2": [
                        password_confirmation_error,
                    ],
                }
            )
