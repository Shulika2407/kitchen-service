from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import (DishType,
                         Dish,
                         Cook,
                         Ingredient,)

DishType_Format_URL = reverse("kitchen:dish-type-list")
Cook_Format_URL = reverse("kitchen:cook-list")
Dish_Format_URL = reverse("kitchen:dish-list")
Ingredient_URL = reverse("kitchen:ingredient-list")


class PublicViewsTest(TestCase):
    def test_login_required(self):
        urls = [
            DishType_Format_URL,
            Cook_Format_URL,
            Dish_Format_URL,
            Ingredient_URL,
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_dishtype(self):
        DishType.objects.create(name="Biscuits")
        DishType.objects.create(name="Braai")
        response = self.client.get(DishType_Format_URL)
        self.assertEqual(response.status_code, 200)
        dishtype = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dishtype)
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_search_dishtype_filters_queryset(self):
        DishType.objects.create(name="Biscuits")
        DishType.objects.create(name="Braai")
        self.client.force_login(self.user)
        response = self.client.get(DishType_Format_URL, {"name": "bi"})
        self.assertContains(response, "Biscuits")
        self.assertNotContains(response, "Braai")


class PrivateIngredientTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_ingredient(self):
        Ingredient.objects.create(name="Spaghetti", calories_per_100g=158)
        Ingredient.objects.create(name="Bacon", calories_per_100g=410)
        response = self.client.get(Ingredient_URL)
        self.assertEqual(response.status_code, 200)
        ingredient = Ingredient.objects.all()
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredient)
        )
        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")

    def test_search_ingredient_filters_queryset(self):
        Ingredient.objects.create(name="Spaghetti", calories_per_100g=158)
        Ingredient.objects.create(name="Bacon", calories_per_100g=410)
        self.client.force_login(self.user)
        response = self.client.get(Ingredient_URL, {"name": "ba"})
        self.assertContains(response, "Bacon")
        self.assertNotContains(response, "Spaghetti")


class PrivateCookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "years_of_experience": 10,
        }
        res = self.client.post(reverse("kitchen:cook-create"), data=form_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(
            username=form_data["username"]).exists())

    def test_search_cook_filters_queryset(self):
        Cook.objects.create_user(
            username="admin", password="Ge12349", years_of_experience=12
        )
        Cook.objects.create_user(
            username="asasha", password="test369", years_of_experience=2
        )

        response = self.client.get(Cook_Format_URL, {"username": "ad"})
        self.assertContains(response, "admin")
        self.assertNotContains(response, "asasha")


class PrivateDishTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_search_dish_filters_queryset(self):
        dish_type = DishType.objects.create(name="Biscuits")
        ingredient = Ingredient.objects.create(name="Spaghetti", calories_per_100g=158)
        Dish.objects.create(name="Spaghetti Carbonara",
                           dish_type=dish_type, ingredients=ingredient)
        Dish.objects.create(name="South African Braai",
                           dish_type=dish_type, ingredients=ingredient)
        self.client.force_login(self.user)
        response = self.client.get(Dish_Format_URL, {"name": "Spa"})
        self.assertContains(response, "Spaghetti Carbonara")
        self.assertNotContains(response, "South African Braai")
