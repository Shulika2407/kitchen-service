from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    calories_per_100g = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.pk})
