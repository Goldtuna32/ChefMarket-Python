from django.shortcuts import render
from .models import Ingredient

# Create your views here.
def ingredient_alphabetical_list():
    
    active_ings = Ingredient.objects.active_ingerdients()
    
    grouped_ing = {}
    for ing in active_ings:
        letter = ing.name[0].upper()
        if letter not in grouped_ing:
            grouped_ing[letter] = []
            
    grouped_ing[letter].append(ing)    
    return grouped_ing

def ing_list(request):
    return render(request,'ingredient_list.html')

def index(request):
    return render(request, 'index.html')

def add_ingredient(request):
    return render(request, 'add_ingredient.html')