from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import Input


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), min_length=8)
    password2 = forms.CharField(label='Повторите', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': Input(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'autofocus': ''}),
            'first_name': Input(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': Input(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': Input(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
        }

    def clean_password2(self):
        cd = self.data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_username(self):
        cd = self.data
        if len(cd['username']) < 6:
            raise forms.ValidationError('Имя пользователя должно содержать 6 символов и более.')
        return cd['username']

    def clean_email(self):
        cd = self.data
        users = User.objects.all()
        for user in users:
            if user.email == cd['email']:
                raise forms.ValidationError('Эта электронная почта уже используется')
        return cd['email']

