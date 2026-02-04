from django.shortcuts import redirect, render
from django.db import transaction

from ChefMarket.recipe.forms import RecipeForm
from .models import Recipe
from ChefMarket.ingredients.models import Ingredient


# Create your views here.
def recipe_list(request):
    return render(request, "recipe_list.html")


def recipe_detail(request, recipe_id):
    return render(request, "recipe_detail.html", {"recipe_id": recipe_id})


def recipe_create(request):
    form = RecipeForm(request.POST or None)
    
    # Checking POST or GET
    if request.method == "POST":
        if form.is_valid():  
            try:
                # Start Communicating and Adding Data to the Database
                with transaction.atomic():
                    recipe = form.save()
            
                return redirect("recipe_detail", recipe_id=recipe.id)
            
            except:
                form.add_error(form.errors)
                
                
    return render(request, "recipe_create.html", {"form": form})