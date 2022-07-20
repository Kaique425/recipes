from collections import defaultdict

from django import forms
from django.forms import ModelForm, ValidationError
from recipes.models import Recipe
from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.errors = defaultdict(list) if errors is None else errors
        self.data = data
        self.clean()

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "preparations_time",
            "preparations_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        )

        widgets = {
            "preparations_time_unit": forms.Select(
                choices=(("Minutes", "Minutes"), ("Hours", "Hours"))
            ),
            "servings_unit": forms.Select(
                choices=(("Portions", "Portions"), ("Person", "Person"))
            ),
            "cover": forms.FileInput(),
        }

    def clean(self, *args, **kwargs):
        self.clean_servings()
        self.clean_preparations_time()
        self.clean_title()

        data = self.data
        title = data.get("title")
        description = data.get("description")

        if title == description:
            self.errors["description"].append("Can not be equal to title")
            self.errors["title"].append("Can not be equal to description")

        if self.errors:
            raise ValidationError(self.errors)

    def clean_title(self):
        title = self.data.get("title")

        if len(title) < 5:
            self.errors["title"].append("Title must have at least 5 characteres.")

        return title

    def clean_preparations_time(self):
        preparations_time = self.data.get("preparations_time")

        if not is_positive_number(preparations_time):
            print(f"Numero do preparation time {preparations_time}")
            self.errors["preparations_time"].append(
                "Preparation time must be a positive number."
            )

        return preparations_time

    def clean_servings(self):
        servings = self.data.get("servings")

        if not is_positive_number(servings):
            self.errors["servings"].append("Servings must be a positive number.")

        return servings
