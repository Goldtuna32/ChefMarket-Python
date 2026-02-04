from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients']
        widgets = {
            'ingredients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if Recipe.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A recipe with this name already exists")
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        ingredients = cleaned_data.get('ingredients')
        
        return cleaned_data