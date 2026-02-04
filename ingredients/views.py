from django.shortcuts import render
from .models import Ingredient

# Create your views here.
def ingredient_list():
    ingredientList = Ingredient.objects.all()
    return ingredientList

def index(request):
    return render(request, 'index.html')

def add_ingredient(request):
    return render(request, 'add_ingredient.html')