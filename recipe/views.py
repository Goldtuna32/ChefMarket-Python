from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from .models import Recipe
from ChefMarket.ingredients.models import Ingredient


# Create your views here.
def recipe_list(request):
    return render(request, "recipe_list.html")


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
