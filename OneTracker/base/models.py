from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class IngredientStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ingredient_id = models.PositiveIntegerField()
    amount = models.FloatField(
        validators=[MinValueValidator(0.0)])
    unit = models.CharField(max_length=50)
    calories = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    carbs = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    fat = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    protein = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    sodium = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    sugar = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    date_purchased = models.DateTimeField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class IngredientHistory(models.Model):
    parent = models.ForeignKey(IngredientStock, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ingredient_id = models.PositiveIntegerField()
    amount = models.FloatField(
        validators=[MinValueValidator(0.0)])
    unit = models.CharField(max_length=50)
    calories = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    carbs = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    fat = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    protein = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    sodium = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    sugar = models.IntegerField(
        validators=[MinValueValidator(0.0)])
    created = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
