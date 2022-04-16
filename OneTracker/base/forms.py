from django.forms import ModelForm
from .models import IngredientStock


class IngredientForm(ModelForm):
    class Meta:
        model = IngredientStock
        fields = '__all__'
        exclude = ["user", "name", "ingredient_id"]
