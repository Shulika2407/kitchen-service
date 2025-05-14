from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.author = get_user_model().objects.create_user(
            username="author",
            password="testauthor",
            first_name="Test",
            last_name="Author",
            years_of_experience=5
        )
        self.author.is_staff = True
        self.author.save()

    def test_author_years_of_experience(self):
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.years_of_experience)


    def test_author_detail_years_of_experience(self):
        url = reverse("admin:kitchen_cook_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.years_of_experience)

    def test_additional_fields_in_fieldsets(self):
        url = reverse("admin:kitchen_cook_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.first_name)
        self.assertContains(res, self.author.last_name)
        self.assertContains(res, self.author.years_of_experience)
