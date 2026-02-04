# ingredient_app/context_processors.py
from .models import Ingredient

def ingredient_list(request):
    # Fetching only ID and Name is much lighter on the database
    return {
        'all_ingredients': Ingredient.objects.all().only('id', 'name').order_by('name')
    }