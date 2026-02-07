from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.ingredient_list, name="ingredient_list"),
    path("", views.index, name="index"),
]
