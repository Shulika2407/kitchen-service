from django.urls import path
from .views import (
    index,
    DishTypeListView,
    DishListView,
    CookListView,
    IngredientListView,
    )


urlpatterns = [
   path("", index, name='index'),
   path("dishtype/",
        DishTypeListView.as_view(),
        name="dish-type-list",
        ),
   path("dish/",
        DishListView.as_view(),
        name="dish-list",
        ),
   path("cook/",
        CookListView.as_view(),
        name="cook-list",
        ),
   path("ingredient/",
        IngredientListView.as_view(),
        name="ingredient-list",
        ),

]

app_name="kitchen"
