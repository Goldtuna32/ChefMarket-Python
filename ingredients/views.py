from django.shortcuts import render

# Create your views here.
def ingredient_list(request):
    return render(request, 'ingredients/ingredient_list.html')

def index(request):
    return render(request, 'index.html')