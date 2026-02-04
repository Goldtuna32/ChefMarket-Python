from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    ingredients = models.ManyToManyField('ingredients.Ingredient')