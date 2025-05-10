from django.test import TestCase
from django.contrib.auth import get_user_model
from kitchen.models import DishType, Ingredient, Cook, Dish


class ModelTest(TestCase):
    def test_dishtype_str(self):
        dish_type = DishType.objects.create(name="Dessert")
        self.assertEqual(str(dish_type), "Dessert")

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="Dessert")
        dish = Dish.objects.create(
            name="Test Dish",
            description="Tasty",
            price=10.50,
            dish_type=dish_type,
        )
        self.assertEqual(str(dish), dish.name)

    def test_cook_with_years_of_experience(self):
        username = "test"
        password = "test123"
        years_of_experience = 5
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(cook.username, username)
        self.assertEqual(cook.years_of_experience, years_of_experience)
        self.assertTrue(cook.check_password(password))
