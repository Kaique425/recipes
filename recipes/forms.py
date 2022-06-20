from collections import defaultdict

from django import forms
from django.forms import ModelForm, ValidationError

from utils.strings import is_positive_number

from .models import Recipe


class RecipeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

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
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        if title == description:
            self._my_errors["description"].append("Can not be equal to title")
            self._my_errors["title"].append("Can not be equal to description")

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            self._my_errors["title"].append("Title must have at least 5 characteres.")

        return title

    def clean_preparations_time(self):
        preparations_time = self.cleaned_data.get("preparations_time")

        if not is_positive_number(preparations_time):
            self._my_errors["preparations_time"].append(
                "Preparation time must be a positive number."
            )

        return preparations_time

    def clean_servings(self):
        servings = self.cleaned_data.get("servings")

        if not is_positive_number(servings):
            self._my_errors["servings"].append("Servings must be a positive number.")

        return servings
