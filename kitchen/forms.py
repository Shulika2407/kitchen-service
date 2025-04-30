from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from kitchen.models import Dish, Ingredient, Cook


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Ingredient.objects.all(),
    )
    class Meta:
        model = Dish
        fields = "__all__"


def validate_years_of_experience(
    years_of_experience,
):
    if years_of_experience <= 0:
        raise ValidationError("years of experience cannot be less than zero")
    if years_of_experience != int(years_of_experience):
        raise ValidationError("years of experience must be an integer")


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):  # this logic is optional, but possible
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = "__all__"

    def clean_license_number(self):  # this logic is optional, but possible
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])
