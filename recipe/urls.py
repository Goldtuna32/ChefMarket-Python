from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_alphabetical_list, name="recipe_list"),
    path("load_more_recipe", views.load_more_by_letter, name="load_more_recipe"),
    path("recipe_detail", views.recipe_detail, name="recipe_detail"),
]
