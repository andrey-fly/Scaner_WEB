from datetime import datetime
import random
import string

import requests
from django.conf import settings
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic.base import View

from API_App.models import Category
from Modules.ImageController import ImageController, Picture, Goods
from WEB_App.forms import UserRegistrationForm, RecoveryPass, AddGoodForm, CreateCategoryForm, ChangeInfoForm, FileForm
from WEB_App.models import Recovery, GoodsOnModeration, UserPhoto

from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    context = {'data': datetime.now()}
    reg_form = UserRegistrationForm()
    errors = []
    if request.method == 'POST':
        if request.POST.get('status') == 'SignUp':
            reg_form = UserRegistrationForm(request.POST)
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
        if request.FILES:
            if not request.user.is_authenticated:
                context['show_modal'] = True
            else:
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
        if good.category:
            self.context['categories'] = good.category.get_family
        return render(request, self.template_name, self.context)


class AddProductPage(View):
    template_name = 'photo/add_product.html'
    context = {}

    def get(self, request):
        img_id = int(request.GET['image'])
        img = Picture.objects.get(id=img_id)
        self.context['img'] = img.file.url
        return render(request, self.template_name, self.context)

    def post(self, request):
        good = GoodsOnModeration(
            name=request.POST.get('name'),
            image=Picture.objects.get(id=int(request.GET['image'])),
            user=request.user
        )

        response = requests.get('http://0.0.0.0/api/v1/getbarcode/',
                                files={'file': good.image.file},
                                # params={'user': request.user.id,
                                #         'platform': 'web'},
                                # headers={'Authorization': 'Token 8cf8bf79233bd6f7cd98cc6e8ef1d6efa69996d6'}
                                ).json()

        if response['status'] == 'ok':
            good.barcode = response['barcode']

        good.save()

        return redirect('/thanks/')


def send_recovery_code(code, user):
    email_subject = 'EVILEG :: Сообщение через контактную форму '
    email_body = "Код для восстановления пароля: {}".format(code)
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['{}'.format(user.email)],
              fail_silently=False)


class AcceptPage(PermissionRequiredMixin, View):
    template_name = 'admin/accept.html'
    permission_required = 'WEB_App.view'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        if request.POST.get('action') == 'accept':
            moderation_good = GoodsOnModeration.objects.get(id=request.POST.get('id'))
            name = request.POST.get('name')
            barcode = request.POST.get('barcode') if request.POST.get('barcode') != 'None' else None
            points = request.POST.get('points') or '?'
            category = None

            if Category.objects.filter(id=request.POST.get('category')):
                category = Category.objects.get(id=request.POST.get('category'))

            new_good = Goods(
                name=name,
                barcode=barcode,
                category=category,
                file=moderation_good.image.file,
                user=request.user,
                points_rusControl=points
            )

            if request.FILES:
                new_good.file = request.FILES.get('image')

            new_good.save()
            moderation_good.status = 2
            moderation_good.save()

        elif request.POST.get('action') == 'deny':
            moderation_good = GoodsOnModeration.objects.get(id=request.POST.get('id'))
            moderation_good.status = 3
            moderation_good.save()

        elif request.POST.get('action') == 'create_category':
            name = request.POST.get('name')
            parent_id = request.POST.get('category') or None
            image = request.FILES.get('image') or None
            parent = None
            if parent_id:
                parent = Category.objects.get(id=parent_id)

            requests.post('http://0.0.0.0/api/v1/category/create/',
                          files={'file': image},
                          data={'user': request.user.id,
                                'name': name,
                                'parent': parent_id,
                                },
                          headers={'Authorization': 'Token 8e96993a6a5b3f9c515b5cc43c3a7083cb8d1897'}
                          )

        return render(request, self.template_name, self.get_context())

    def get_context(self):
        context = {}

        data_goods_on_moderation = GoodsOnModeration.objects.filter(status=1)
        context['goods_data'] = data_goods_on_moderation

        categories = Category.objects.all()
        context['categories'] = categories
        return context


def profile(request):
    context = {}
    context['user'] = User.objects.get(id=request.user.id)
    current_user = User.objects.get(id=request.user.id)
    if UserPhoto.objects.filter(user=current_user):
        context['photo'] = UserPhoto.objects.get(user=current_user).img
    else:
        context['photo'] = 'profile/profile_icon.png'
    return render(request, 'profile/profile.html', context)


def change_info(request):
    current_user = User.objects.get(id=request.user.id)
    form = ChangeInfoForm(request.POST)
    form.fields['username'].widget.attrs['placeholder'] = current_user.username
    form.fields['email'].widget.attrs['placeholder'] = current_user.email
    photo = FileForm(request.POST, request.FILES)
    context = {'form': form, 'photo': photo}
    if UserPhoto.objects.filter(user=current_user):
        context['userphoto'] = UserPhoto.objects.get(user=current_user).img
    else:
        context['userphoto'] = 'profile/profile_icon.png'
    if request.method == 'POST':
        if request.POST.get('old_password'):
            old_password = request.POST.get('old_password')
            if current_user.check_password('{}'.format(old_password)) is False:
                form.set_old_password_flag()
                return render(request, 'profile/change_info.html', {'form': form})
        if form.is_valid():
            if request.POST.get('username'):
                current_user.username = request.POST.get('username')
            if request.POST.get('email'):
                current_user.email = request.POST.get('email')
            if request.POST.get('old_password'):
                old_password = request.POST.get('old_password')
                if current_user.check_password('{}'.format(old_password)) is False:
                    form.set_old_password_flag()
                    return render(request, 'profile/change_info.html', {'form': form})
                else:
                    current_user.set_password('{}'.format(form.data['new_password2']))
            current_user.save()
            login(request, current_user)
        else:
            return render(request, 'profile/change_info.html', context)
        if photo.is_valid():
            if UserPhoto.objects.filter(user=current_user):
                userphoto = UserPhoto.objects.get(user=current_user)
            else:
                userphoto = UserPhoto(user=current_user, img='profile/profile_icon.png')
            if request.FILES.get('file'):
                userphoto.img = request.FILES.get('file')
                userphoto.save()
    if request.POST.get('status'):
        return redirect('/profile')
    return render(request, 'profile/change_info.html', context)
