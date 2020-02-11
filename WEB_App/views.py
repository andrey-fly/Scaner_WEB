from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render

from WEB_App.forms import UserRegistrationForm


def index(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            login(request, new_user)
            print(User.objects.get(username='Ender'))
            return render(request, 'index.html', {'username': user_form.data['username']})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'index.html', {'user_form': user_form})
