from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import Input

from WEB_App.models import Comment, ChildrenComment


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'id': 'reg-input', 'class': 'mb-2', 'placeholder': 'Пароль'}),
                               min_length=8)
    password2 = forms.CharField(label='Повторите',
                                widget=forms.PasswordInput(attrs={'id': 'reg-input', 'class': 'mb-2', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': Input(attrs={'id': 'reg-input', 'class': 'mb-2', 'placeholder': 'Имя'}),
            'email': Input(attrs={'id': 'reg-input', 'class': 'mb-2', 'placeholder': 'Почта'})
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


class ChangeInfoForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',
                               min_length=3,
                               required=False,
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Ваше имя',
                                       'id': 'name'}
                               )
                               )
    email = forms.EmailField(label='Электронная почта',
                             required=False,
                             widget=forms.EmailInput(
                                 attrs={
                                     'placeholder': 'Email',
                                     'id': 'email'}
                             )
                             )
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput, required=False, initial=None)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, min_length=8, required=False,
                                   initial=None)
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, required=False, initial=None)
    old_password_flag = True

    def set_old_password_flag(self):
        self.old_password_flag = False

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not old_password and self.data.get('new_password'):
            print('Not')
            raise forms.ValidationError("Вы должны ввести Ваш старый пароль.")
        if self.old_password_flag is False:
            raise forms.ValidationError("Старый пароль, который Вы ввели, - неверен.")
        return old_password

    def clean_new_password2(self):
        new_password = self.cleaned_data.get('new_password')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password != new_password2:
            raise forms.ValidationError('Новые пароли не совпадают.')
        return new_password2


class FileForm(forms.Form):
    file = forms.FileField(label='Select a file', required=False,
                           widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'inputGroupFile',
                                                         'aria-describedby': "inputGroupFileBtn"}))


class BarcodeForm(forms.Form):
    barcode = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputBarcode',
        'placeholder': " ",
        'aria-describedby': 'question-barcode',
    }))


class ComplaintForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputTitle',
        'placeholder': "Дайте кратки заголовок",
    }), max_length=255)
    text = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputText',
        'placeholder': "Опишите проблему",
    }))


class ComplaintResponseForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputText',
        'placeholder': "Ваш ответ на жалобу",
    }))
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text',)
#         widgets = {
#             'text': Input(attrs={'class': 'form-control', 'placeholder': 'Описание', 'style': 'width: auto !important; border-radius: 8px'}),
#         }


# class RatePhotoForm(forms.Form):
#     rate = forms.ChoiceField(widget=forms.Select(), required=True)
