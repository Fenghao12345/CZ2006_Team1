from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #to add user to database
            #the validated form data will be in form.cleaned_data dictionary
            username = form.cleaned_data.get('username') 
            #flash massage
            messages.success(request, f'Yor account has been created! You are now able to log in')
            return redirect('login') #name of url pattern

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')