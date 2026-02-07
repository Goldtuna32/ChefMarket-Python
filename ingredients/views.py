from django.http import JsonResponse
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


# Fetch ing list
def ing_list(request):

    # Grouped ing from list
    grouped_ing = ingredient_alphabetical_list()

    return render(request, "ingredient_list.html", {"grouped_ing": grouped_ing})


def index(request):
    return render(request, "index.html")


def add_ingredient(request):
    return render(request, "add_ingredient.html")


def load_more_(request):
    letter = request.GET.get("letter")
    offset = int(request.GET.get("offset", 10))

    more_ing = (
        Ingredient.objects.active_ingerdients()
        .filter(name__isstartwith=letter)
        .order_by("name")[offset : offset + 10]
    )

    data = [{"id": i.id, "name": i.name} for i in more_ing]
    return JsonResponse({"active_ing": data, "has_more": len(data) == 10})
