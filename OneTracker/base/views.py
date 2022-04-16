from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import IngredientHistory, IngredientStock
from .forms import IngredientForm
import pytz
from datetime import datetime
import requests

# Create your views here.

def test(request):
    return render(request, 'base/base.html')


def home(request):
    page = 'home'

    if request.user.is_authenticated:
        time_zone = pytz.timezone("Asia/Singapore")
        today = datetime.utcnow()
        today = today.replace(tzinfo=pytz.utc)
        today = today.replace(tzinfo=pytz.utc)
        today = today.astimezone(time_zone)
        ingredients_history = IngredientHistory.objects.filter(
            user=request.user,
            type="Consumed",
            created__date=today
        )
        print(today)
        calories = 0
        carbs = 0
        fat = 0
        protein = 0
        sodium = 0
        sugar = 0
        for ingredient_history in ingredients_history:
            calories += float(ingredient_history.calories)
            carbs += float(ingredient_history.carbs)
            fat += float(ingredient_history.fat)
            protein += float(ingredient_history.protein)
            sodium += float(ingredient_history.sodium)
            sugar += float(ingredient_history.sugar)

            calories = int(calories)
            carbs = int(carbs)
            fat = int(fat)
            protein = int(protein)
            sodium = int(sodium)
            sugar = int(sugar)

        context = {'page': page, "calories": calories, "carbs": carbs,
                   "fat": fat, "protein": protein, "sodium": sodium, "sugar": sugar}
        return render(request, 'base/home.html', context)

    context = {'page': page}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/home.html')


@login_required(login_url='login')
def stock(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    ingredients = IngredientStock.objects.filter(
        Q(name__icontains=q),
        user=request.user
    )

    ingredients_count = ingredients.count()

    context = {"ingredients": ingredients,
               "ingredients_count": ingredients_count}
    return render(request, 'base/stock.html', context)


@login_required(login_url='login')
def purchase(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if q:
        url = f"https://api.spoonacular.com/food/ingredients/search?query={q}&apiKey={settings.API_KEY}&number=100"

        r = requests.get(url)
        results = r.json() if r.status_code == 200 else None

        if results:
            for item in results["results"]:
                item["name"] = item["name"].title()
            context = {'results': results}
            return render(request, 'base/purchase.html', context)

    return render(request, 'base/purchase.html')


@login_required(login_url='login')
def addIngredients(request):
    page = 'add_ingredients'
    form = IngredientForm()
    q = request.GET.get('q')
    amount = request.GET.get('amount') if request.GET.get(
        'amount') != None else ''
    unit = request.GET.get('unit') if request.GET.get('unit') != None else ''

    if amount and unit:
        page = 'ingredients_information'
        url = f"https://api.spoonacular.com/food/ingredients/{q}/information?amount={amount}&unit={unit}&apiKey={settings.API_KEY}"
    else:
        url = f"https://api.spoonacular.com/food/ingredients/{q}/information?amount=100&unit=g&apiKey={settings.API_KEY}"

    r = requests.get(url)
    results = r.json()

    results["name"] = results["name"].title()
    units = results["possibleUnits"]

    nutrients_lst = results["nutrition"]["nutrients"]
    nutrient_names1 = ["Calories", "Fat", "Saturated Fat",
                       "Poly Unsaturated Fat", "Mono Unsaturated Fat", "Cholesterol"]
    nutrient_names2 = ["Sodium", "Potassium",
                       "Carbohydrates", "Fiber", "Sugar", "Protein"]
    nutrient_names3 = ["Vitamin A", "Vitamin C"]
    nutrient_names4 = ["Calcium", "Iron"]
    nutrients1 = []
    nutrients2 = []
    nutrients3 = []
    nutrients4 = []

    for name in nutrient_names1:
        try:
            nutrients1.append(nutrients_lst[next((index for (index, d) in enumerate(
                nutrients_lst) if d["name"] == name), None)])
        except TypeError:
            nutrients1.append({"name": name, "amount": '0', "unit": 'g'})

    for name in nutrient_names2:
        try:
            nutrients2.append(nutrients_lst[next((index for (index, d) in enumerate(
                nutrients_lst) if d["name"] == name), None)])
        except TypeError:
            nutrients2.append({"name": name, "amount": '0', "unit": 'g'})

    for name in nutrient_names3:
        try:
            nutrients3.append(nutrients_lst[next((index for (index, d) in enumerate(
                nutrients_lst) if d["name"] == name), None)])
        except TypeError:
            nutrients3.append({"name": name, "amount": '0', "unit": 'g'})

    for name in nutrient_names4:
        try:
            nutrients4.append(nutrients_lst[next((index for (index, d) in enumerate(
                nutrients_lst) if d["name"] == name), None)])
        except TypeError:
            nutrients4.append({"name": name, "amount": '0', "unit": 'g'})

    if request.method == "POST":
        amount = request.POST.get("amount")
        unit = request.POST.get("units")
        form = IngredientForm(request.POST)

        url = f"https://api.spoonacular.com/food/ingredients/{q}/information?amount={amount}&unit={unit}&apiKey={settings.API_KEY}"
        r = requests.get(url)
        results = r.json()

        results["name"] = results["name"].title()

        nutrients_lst = results["nutrition"]["nutrients"]
        nutrient_names = ["Calories", "Carbohydrates", "Fat",
                          "Protein", "Sodium", "Sugar"]
        nutrients = []

        for name in nutrient_names:
            try:
                nutrients.append(nutrients_lst[next((index for (index, d) in enumerate(
                    nutrients_lst) if d["name"] == name), None)])
            except TypeError:
                nutrients.append({"name": name, "amount": '0', "unit": 'g'})

        ingredient_stock = IngredientStock.objects.create(
            user=request.user,
            name=results["name"],
            ingredient_id=q,
            amount=amount,
            unit=unit,
            calories=nutrients[0]["amount"],
            carbs=nutrients[1]["amount"],
            fat=nutrients[2]["amount"],
            protein=nutrients[3]["amount"],
            sodium=nutrients[4]["amount"],
            sugar=nutrients[5]["amount"],
            date_purchased=datetime.now(),
        )

        IngredientHistory.objects.create(
            parent=ingredient_stock,
            type="Purchased",
            user=request.user,
            name=results["name"],
            ingredient_id=q,
            amount=amount,
            unit=unit,
            calories=nutrients[0]["amount"],
            carbs=nutrients[1]["amount"],
            fat=nutrients[2]["amount"],
            protein=nutrients[3]["amount"],
            sodium=nutrients[4]["amount"],
            sugar=nutrients[5]["amount"],
            created=datetime.now(),
        )
        return redirect(request.POST.get('previous'))

    context = {'page': page, 'amount': amount, 'unit': unit, 'form': form, 'results': results, 'units': units, 'nutrients1': nutrients1,
               'nutrients2': nutrients2, 'nutrients3': nutrients3, 'nutrients4': nutrients4}
    return render(request, 'base/ingredients_form.html', context)


@login_required(login_url='login')
def deleteIngredients(request, pk):
    ingredient = IngredientStock.objects.get(id=pk)

    if request.method == "POST":
        ingredient.delete()
        return redirect('stock')

    return render(request, 'base/delete_ingredient.html', {'obj': ingredient})


@login_required(login_url='login')
def consume(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    ingredients = IngredientStock.objects.filter(
        Q(name__icontains=q),
        user=request.user
    )

    if request.method == "POST":
        amounts = request.POST.getlist("amount")
        ids = request.POST.getlist("id")

        for i in range(len(amounts)):
            if amounts[i] == '0.0':
                continue

            ingredient_stock = IngredientStock.objects.get(pk=ids[i])
            ingredient_stock.amount = str(
                float(ingredient_stock.amount) - float(amounts[i]))
            ingredient_stock.save()
            print(ingredient_stock.unit)

            url = f"https://api.spoonacular.com/food/ingredients/{ingredient_stock.ingredient_id}/information?amount={amounts[i]}&unit={ingredient_stock.unit}&apiKey={settings.API_KEY}"
            r = requests.get(url)
            results = r.json()

            nutrients_lst = results["nutrition"]["nutrients"]
            nutrient_names = ["Calories", "Carbohydrates", "Fat",
                              "Protein", "Sodium", "Sugar"]
            nutrients = []

            for name in nutrient_names:
                try:
                    nutrients.append(nutrients_lst[next((index for (index, d) in enumerate(
                        nutrients_lst) if d["name"] == name), None)])
                except TypeError:
                    nutrients.append(
                        {"name": name, "amount": '0', "unit": 'g'})

            IngredientHistory.objects.create(
                parent=ingredient_stock,
                type="Consumed",
                user=request.user,
                name=ingredient_stock.name,
                ingredient_id=ingredient_stock.ingredient_id,
                amount=amounts[i],
                unit=ingredient_stock.unit,
                calories=nutrients[0]["amount"],
                carbs=nutrients[1]["amount"],
                fat=nutrients[2]["amount"],
                protein=nutrients[3]["amount"],
                sodium=nutrients[4]["amount"],
                sugar=nutrients[5]["amount"],
                created=datetime.now(),
            )

    context = {"ingredients": ingredients}
    return render(request, 'base/consume.html', context)


@login_required(login_url='login')
def history(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    ingredients_history = IngredientHistory.objects.filter(
        Q(name__icontains=q),
        user=request.user,
        
    )

    context = {"ingredients_history": ingredients_history}
    return render(request, 'base/history.html', context)

@login_required(login_url='login')
def purchasehistory(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    ingredients_history = IngredientHistory.objects.filter(
        Q(name__icontains=q, type='Purchased'),
        user=request.user,
        
    )

    context = {"ingredients_history": ingredients_history}
    return render(request, 'base/history.html', context)

@login_required(login_url='login')
def consumehistory(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    ingredients_history = IngredientHistory.objects.filter(
        Q(name__icontains=q, type='Consumed'),
        user=request.user,
        
    )

    context = {"ingredients_history": ingredients_history}
    return render(request, 'base/history.html', context)