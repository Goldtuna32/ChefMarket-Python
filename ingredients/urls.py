from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ing_list, name='ingredient_list'),
    path('', views.add_ingredient, name='add_ingredient'),
]