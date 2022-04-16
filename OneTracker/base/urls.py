from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name="test"), 

    path('', views.home, name="home"), 
    path('about/', views.about, name="about"),


    path('stock/', views.stock, name="stock"),
    path('purchase/', views.purchase, name="purchase"),
    path('add-ingredients/', views.addIngredients, name="add-ingredients"),
    path('delete-ingredients/<str:pk>/', views.deleteIngredients, name="delete-ingredients"),
    path('consume/', views.consume, name="consume"),
    path('history/', views.history, name="history"),
    path('consumehistory/', views.consumehistory, name="consumehistory"),
    path('purchasehistory/', views.purchasehistory, name="purchasehistory"),
]
