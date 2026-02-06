from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
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

# Load More Recipe by letter adding 10 offset to current one
def load_more_by_letter(request):
    letter = request.GET.get("letter")
    offset = int(request.GET.get("offset", 10))

    more_recipes = Recipe.objects.filter(name__isstartswith=letter).order_by("name")[
        offset : offset + 10
    ]

    data = [{"id": r.id, "name": r.name} for r in more_recipes]
    
    return JsonResponse({'recipes': data, 'has_more': len(data) == 10})



# Fetching Recipe Detail
def recipe_detail(request, recipe_id):
    
    # using 'prefetch_related' making ingredients looting faster
    recipe = get_object_or_404(Recipe.objects.prefetch_related('ingredients'), id=recipe_id)
    
    #condition if recipe existed or not
    if not recipe:
        return render(request,"error.html", {
            "errors": "failed to load the recipe"
        })
    return render(request, "recipe_detail.html", {"recipe": recipe})


def recipe_create(request):
    if request.method == "POST":

        # Adding Recipe with Ingredients
        recipe_name = request.POST.get("recipe_name")
        recipe_description = request.POST.get("recipe_description")
        ingredients_id = request.POST.getlist("ingredients")

        # Checking that ingredients are selected
        if not ingredients_id:
            return render(request,
                "recipe_create.html",
                {"error": "At least one ingredient must be selected.",
                 },
                
            )

    # checking that ingredients are not empty
    try:
        with transaction.atomic():
            recipe = Recipe.objects.create(
                name=recipe_name, description=recipe_description
            )
            
            # Linking Ingredients to Recipe
            valid_ingredients = Ingredient.objects.filter(id__in=ingredients_id)
            recipe.ingredients.add(*valid_ingredients)

            # Return to recipe list after successful creation
            return redirect("recipe_list")

    # Return Error if something goes wrong
    except Exception as e:
        return render(request, "recipe_create.html", {"error": str(e)})

    # If GET request, render the creation form
    return render(request, "recipe_create.html", {"ingredients": all_ingredients})
