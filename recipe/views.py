from django.shortcuts import redirect, render
from django.db import transaction
from django.http import JsonResponse

from ChefMarket.recipe.forms import RecipeForm
from .models import Recipe
from ChefMarket.ingredients.models import Ingredient


# Create your views here.

# Fetch 10 Recipes from Each Alphabet
def recipe_alphabetical_list(request):
    all_recipes = Recipe.objects.all().order_by("name")

    grouped_recipes = {}
    for recipe in all_recipes:
        letter = recipe.name[0].upper()
        if letter not in grouped_recipes:
            grouped_recipes[letter] = []

        if len(grouped_recipes[letter]) < 10:
            grouped_recipes[letter].append(recipe)
    return render(request, "recipe_list.html", {"grouped_recipes": grouped_recipes})


def recipe_detail(request, recipe_id):
    return render(request, "recipe_detail.html", {"recipe_id": recipe_id})


#Recipe Create Using Djangon-Forms
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

# Load More Recipe by letter adding 10 offset to current one
def load_more_by_letter(request):
    letter = request.GET.get("letter")
    offset = int(request.GET.get("offset", 10))

    more_recipes = Recipe.objects.filter(name__isstartswith=letter).order_by("name")[
        offset : offset + 10
    ]

    data = [{"id": r.id, "name": r.name} for r in more_recipes]
    
    return JsonResponse({'recipes': data, 'has_more': len(data) == 10})
