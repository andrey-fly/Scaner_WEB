from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import Input


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'mb-2', 'placeholder': 'Пароль'}),
                               min_length=8)
    password2 = forms.CharField(label='Повторите',
                                widget=forms.PasswordInput(attrs={'class': 'mb-2', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': Input(attrs={'class': 'mb-2', 'placeholder': 'Имя'}),
            'email': Input(attrs={'class': 'mb-2', 'placeholder': 'Почта'}),
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


class RecoveryPass(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'autofocus': ''}), min_length=8, required=True)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}), required=True)

    def clean_password2(self):
        cd = self.data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
