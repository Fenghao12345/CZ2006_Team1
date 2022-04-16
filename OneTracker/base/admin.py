from django.contrib import admin
from .models import IngredientStock, IngredientHistory

# Register your models here.
admin.site.register(IngredientStock)
admin.site.register(IngredientHistory)
