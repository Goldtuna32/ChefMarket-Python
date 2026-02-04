from django.db import models

# Create your models here.
class IngredientManager(models.Manager):
    def active_ingerdients(self):
        return self.filter(is_active=True).order_by('name')

class Ingredient(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    quantity = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    objects = IngredientManager()
    