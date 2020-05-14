from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import Input


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={'id': 'reg-input', 'class': 'mb-2',
                                          'placeholder': 'Пароль'}),
                               min_length=8)
    password2 = forms.CharField(label='Повторите',
                                widget=forms.PasswordInput(
                                    attrs={'id': 'reg-input', 'class': 'mb-2',
                                           'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': Input(attrs={'id': 'reg-input', 'class': 'mb-2', 'placeholder': 'Имя'}),
            'email': Input(attrs={'id': 'reg-input', 'class': 'mb-2', 'placeholder': 'Почта'})
        }

    def clean_password2(self):
        clear_data = self.data
        if clear_data['password'] != clear_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return clear_data['password2']

    def clean_username(self):
        clear_data = self.data
        if len(clear_data['username']) < 6:
            raise forms.ValidationError('Имя пользователя должно содержать 6 символов и более.')
        return clear_data['username']

    def clean_email(self):
        clear_data = self.data
        users = User.objects.all()
        for user in users:
            if user.email == clear_data['email']:
                raise forms.ValidationError('Эта электронная почта уже используется')
        return clear_data['email']


class RecoveryPass(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'autofocus': ''}), min_length=8,
                               required=True)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}), required=True)

    def clean_password2(self):
        clear_data = self.data
        if clear_data['password'] != clear_data['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return clear_data['password2']


class ChangeInfoForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',
                               min_length=3,
                               required=False,
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Ваше имя',
                                       'id': 'name',
                                       'style': 'max-width: inherit'}
                               )
                               )
    email = forms.EmailField(label='Электронная почта',
                             required=False,
                             widget=forms.EmailInput(
                                 attrs={
                                     'placeholder': 'Email',
                                     'id': 'email',
                                     'style': 'max-width: inherit'}
                             )
                             )
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(
        attrs={'style': 'max-width: inherit'}), required=False, initial=None)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(
        attrs={'style': 'max-width: inherit'}), min_length=8, required=False,
                                   initial=None)
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'style': 'max-width: inherit'}), required=False, initial=None)
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
    file = forms.FileField(label='', required=False,
                           widget=forms.FileInput(
                               attrs={'type': 'file', 'class': 'custom-file-input',
                                      'id': 'inputGroupFile',
                                      'aria-describedby': 'inputGroupFileAddon',
                                      'accept': 'image/*', 'onchange': 'preview_image(event)',
                                      'style': 'display: none'}))


class BarcodeForm(forms.Form):
    barcode = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'inputBarcode',
        'placeholder': " ",
        'aria-describedby': 'question-barcode',
    }))


class ComplaintForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': ' input2',
        'name': 'header',
        'id': 'inputTitle',
        # 'placeholder': "Дайте кратки заголовок",
    }), max_length=255)
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': ' input2',
        'name': 'message',
        'id': 'inputText',
        # 'placeholder': "Опишите проблему",
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
