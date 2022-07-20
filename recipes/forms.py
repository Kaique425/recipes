from collections import defaultdict

from authors.validators import AuthorRecipeValidator
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
        AuthorRecipeValidator(data=super_clean, ErrorClass=ValidationError)
        cleaned_data = self.cleaned_data

        return super_clean
