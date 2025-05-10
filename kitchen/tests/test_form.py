from kitchen.forms import CookCreationForm
from django.test import TestCase


class FormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "years_of_experience": 5,
        }

    def test_driver_create_form_valid(self):
        form = CookCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"],
                         self.form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"],
                         self.form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"],
                         self.form_data["last_name"])
        self.assertEqual(form.cleaned_data["years_of_experience"],
                         self.form_data["years_of_experience"])