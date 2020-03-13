import os
import urllib
from datetime import datetime
import random
import string

import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic.base import View

from Modules.ImageController import ImageController, Picture, Goods
from WEB_App.forms import UserRegistrationForm, RecoveryPass
from WEB_App.models import Recovery, GoodsInModeration

from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.template import RequestContext


def index(request):
    context = {'data': datetime.now()}
    reg_form = UserRegistrationForm()
    errors = []
    if request.method == 'POST':
        if request.POST.get('status') == 'SignUp':
            reg_form = UserRegistrationForm(request.POST)
            print(reg_form.data)
            if reg_form.is_valid():
                new_user = reg_form.save(commit=False)
                new_user.set_password(reg_form.cleaned_data['password2'])
                new_user.save()
                login(request, new_user)
        if request.POST.get('status') == 'SignIn':
            identification = request.POST.get('identification')
            password = request.POST.get('password')

            user = None
            if User.objects.filter(username=identification):
                user = User.objects.get(username=identification)
            elif User.objects.filter(email=identification):
                user = User.objects.get(email=identification)
            if user is None:
                errors.append('Пользователь не найден!')
            elif user.check_password(password) is False:
                errors.append('Неправильный пароль!')
            else:
                login(request, user)

    context['reg_form'] = reg_form
    context['login_errors'] = errors

    return render(request, 'main/index.html', context)


def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            login(request, new_user)
            return render(request, 'main/index.html', {'username': user_form.data['username']})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


def recovery_password(request):
    context = {'step': '1'}
    user_ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
    form = RecoveryPass(request.POST)
    if request.method == 'POST':
        if request.POST.get('start_procedure'):
            data = request.POST.get('start_procedure')
            target_user = None
            if User.objects.filter(username=data):
                target_user = User.objects.get(username=data)
            elif User.objects.filter(email=data):
                target_user = User.objects.get(email=data)
            if target_user:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                send_recovery_code(code, target_user)
                rec = Recovery(target_user=target_user, from_ip=user_ip, code=code)
                rec.save()
                context['step'] = '2'
            else:
                context['error'] = 'Пользователь не найден'
        if request.POST.get('code'):
            code = request.POST.get('code')
            target_user = None
            if Recovery.objects.filter(code=code):
                data = Recovery.objects.filter(code=code)
                for item in data:
                    if user_ip == item.from_ip:
                        target_user = item.target_user
                        context['step'] = '3'
                        context['form'] = form
                        request.session['id_user'] = target_user.id
            if target_user is None:
                context['step'] = '2'
                context['error'] = 'Неверный код'
        if request.POST.get('password'):
            if form.is_valid():
                target_user = request.session.get('id_user')
                new_pass = form.data['password']
                target_user = User.objects.get(id=target_user)
                target_user.set_password(new_pass)
                target_user.save()
                login(request, target_user)
                data_for_delete = Recovery.objects.filter(target_user=target_user)
                for item in data_for_delete:
                    item.delete()
                context['step'] = '4'
            else:
                context['step'] = '3'
                context['form'] = form
                context['error'] = 'Ошибка при заполнении полей'
    return render(request, 'registration/recovery_password.html', context)


class PhotoPage(TemplateView):
    context = {}

    def post(self, request):
        # TODO: Перевести вызов в JS
        response = requests.get('http://0.0.0.0/api/v1/goods/get_product/',
                                files={'file': request.FILES['file']},
                                params={'user': request.user.id,
                                        'platform': 'web'},
                                # headers={'Authorization': 'Token 8cf8bf79233bd6f7cd98cc6e8ef1d6efa69996d6'}
                                )
        response = response.json()
        if response['status'] == 'ok':
            return redirect(to='/product/{}/?image={}'.format(response['good'], response['image']))
        else:
            return redirect(to='/add_product/?image={}'.format(response['image']))


class ProductPage(TemplateView):
    context = {}

    def get(self, request, good):
        img_id = int(request.GET['image'])
        good = Goods.objects.get(name=good)
        img = Picture.objects.get(id=img_id)
        self.context['img'] = img.file.url
        self.context['name'] = good.name
        self.context['positives'] = good.get_positives()
        self.context['negatives'] = good.get_negatives()
        self.context['points'] = good.points_rusControl
        return render(request, self.template_name, self.context)


class AddProductPage(View):
    template_name = 'main/add_product.html'
    context = {}

    def get(self, request):
        img_id = int(request.GET['image'])
        img = Picture.objects.get(id=img_id)
        self.context['img'] = img.file.url
        return render(request, self.template_name, self.context)

    def post(self, request):
        GoodsInModeration(
            name=request.POST.get('name'),
            image=Picture.objects.get(id=int(request.GET['image'])),
            user=request.user
        ).save()
        return redirect('/thanks/')


def send_recovery_code(code, user):
    email_subject = 'EVILEG :: Сообщение через контактную форму '
    email_body = "Код для восстановления пароля: {}".format(code)
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['{}'.format(user.email)],
              fail_silently=False)


def error_403(request, exception):
    context = {}
    return render(request, 'errors/403.html', context)


def error_404(request, exception):
    context = {}
    return render(request, 'errors/404.html', context)


def error_500(request):
    context = {}
    return render(request, 'errors/500.html', context)