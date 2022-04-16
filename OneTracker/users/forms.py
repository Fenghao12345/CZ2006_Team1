from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm): #new form UserRegistrationForm that inherits from UserCreationForm
    email = forms.EmailField() #add a new field

    #if do a form.save it is going to save it to user model and the fields stated in list
    class Meta: #keeps configurations in one place
        #model that will be affectedd
        model = User 
        #field and order showed on form
        fields = ['username', 'email', 'password1', 'password2']