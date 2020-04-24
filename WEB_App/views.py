from datetime import datetime
from PIL import Image
import imagehash
import random
import string

import requests
from django.conf import settings
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Avg, Q, QuerySet
from django.shortcuts import render, redirect
from django.views.generic.base import View

from Scanner.settings import API_TOKEN, API_HEADERS
from WEB_App.forms import *
from WEB_App.models import *

from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http import HttpResponse

from Modules.requests import *


class UserAuth:
    def __init__(self, request, template_name):
        self.template_name = template_name
        self.request = request
        self.reg_form = UserRegistrationForm()
        self.errors = []

    def sign_up(self):
        new_user = self.reg_form.save(commit=False)
        new_user.set_password(self.reg_form.cleaned_data['password2'])
        new_user.save()
        login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')

    def sign_in(self):
        identification = self.request.POST.get('identification')
        password = self.request.POST.get('password')
        user = None
        if User.objects.filter(username=identification):
            user = User.objects.get(username=identification)
        elif User.objects.filter(email=identification):
            user = User.objects.get(email=identification)
        if user is None:
            self.errors.append('Пользователь не найден!')
        elif user.check_password(password) is False:
            self.errors.append('Неправильный пароль!')
        else:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

    def check_auth(self):
        if self.request.POST.get('status') == 'SignUp':
            self.reg_form = UserRegistrationForm(self.request.POST)
            if self.reg_form.is_valid():
                self.sign_up()
        elif self.request.POST.get('status') == 'SignIn':
            self.sign_in()
        return self.reg_form, self.errors


class BaseView(View):
    template_name = 'main/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)

    def check_auth(self, request):
        auth = UserAuth(request, self.template_name)
        return auth.check_auth()


class BaseTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)

    def check_auth(self, request):
        auth = UserAuth(request, self.template_name)
        return auth.check_auth()


class IndexPage(BaseTemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not request.user.is_authenticated:
            reg_form = UserRegistrationForm()
            context['reg_form'] = reg_form
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        if not request.user.is_authenticated:
            context['reg_form'], context['login_errors'] = self.check_auth(request)
        if request.FILES:
            image = request.FILES.get('file')
            if request.user.is_authenticated:
                status_code, response = get_product(image, request.user.username)
            else:
                status_code, response = get_product(image, 'AnonymousUser')
            if response['status'] == 'ok':
                return redirect(to='/product/{}/?image={}'.format(response['good_name'], response['image_hash']))
            else:
                return redirect(to='/add_product/?image={}'.format(response['image_hash']))
        return render(request, self.template_name, context)


class AddProductPage(BaseView):
    template_name = 'photo/add_product.html'

    def get_image_url(self, request):
        own_hash = request.GET.get('image')
        status_code, response = get_picture_by_hash(own_hash)
        return response['file']

    def get(self, request):
        context = {'img': self.get_image_url(request)}
        if not request.user.is_authenticated:
            reg_form = UserRegistrationForm()
            context['reg_form'] = reg_form
        return render(request, self.template_name, context)

    def post(self, request):
        context = {'img': self.get_image_url(request)}
        if not request.user.is_authenticated:
            context['reg_form'], context['login_errors'] = self.check_auth(request)
            context['show_modal'] = True
            return render(request, self.template_name, context)

        image = download_by_hash(request.GET.get('image'))
        barcode = get_barcode(image.content)
        own_hash = request.GET.get('image')
        name = request.POST.get('name')
        status_code, response = create_moderation_good_with_hash(own_hash, name, barcode)
        if status_code == 200:
            return redirect('/thanks/')
        else:
            return redirect('500.html')


class ProductPage(BaseView):
    template_name = 'photo/product.html'

    def get_image_by_hash(self, image_hash):
        status_code_image, response_image = get_picture_by_hash(image_hash)
        return response_image['file']

    def get_list_of_images(self, good_name):
        status_code, response = get_picture_list_by_good_name(good_name)
        data = []
        for image in response:
            data.append(image['file'])
        return data

    def get(self, request, good):
        context = {}
        if not request.user.is_authenticated:
            reg_form = UserRegistrationForm()
            context['reg_form'] = reg_form

        context['name'] = good
        status_code, response = get_good_by_name(good)
        context['default_img'] = response['image']

        if request.GET.get('image'):
            image_hash = request.GET.get('image')
            context['default_img'] = self.get_image_by_hash(image_hash)

        images = self.get_list_of_images(good)[:3]
        context['images'] = images
        context['positives'] = response['positives']
        context['negatives'] = response['negatives']
        context['points'] = response['points']
        context['categories'] = response['categories']
        context['comments'] = Comment.objects.filter(good=good)
        context['show_thanks'] = False

        if request.user.is_authenticated:
            try:
                if Rate.objects.filter(Q(user=request.user) & Q(good=good)):
                    context['rated'] = str(
                        float('{:.2f}'.format(Rate.objects.filter(good=good).aggregate(Avg('rating'))['rating__avg'])))
            except Exception as exc:
                print(exc.args)
        else:
            try:
                if Rate.objects.filter(Q(good=good)):
                    context['rated'] = str(
                        float('{:.2f}'.format(Rate.objects.filter(good=good).aggregate(Avg('rating'))['rating__avg'])))
            except Exception as exc:
                print(exc.args)

        return render(request, self.template_name, context)

    def post(self, request, good):
        context = {'name': good, 'show_thanks': False}
        if not request.user.is_authenticated:
            context['reg_form'], context['login_errors'] = self.check_auth(request)
        else:
            if request.POST.get('comment'):
                new_comment = Comment(
                    text=request.POST.get('comment'),
                    user=request.user,
                    good=good
                )
                new_comment.save()
            if request.POST.get('response-to-comment'):
                new_children_comment = ChildrenComment(
                    text=request.POST.get('response-to-comment'),
                    user=request.user,
                    parent=Comment.objects.get(id=request.POST.get('comment_id'))
                )
                new_children_comment.save()
            if request.POST.get('rating'):
                new_rating = Rate(
                    user=request.user,
                    rating=request.POST.get('rating'),
                    good=good
                )
                new_rating.save()

            post_images = request.FILES.getlist('file')
            if post_images:
                for image in post_images:
                    PictureOnModeration(image=image, target_good=good, user=request.user).save()
                    context['status'] = 'ok'
                    context['show_thanks'] = True
            else:
                context['status'] = 'error'

        context['name'] = good
        status_code, response = get_good_by_name(good)
        context['default_img'] = response['image']

        if request.GET.get('image'):
            image_hash = request.GET.get('image')
            context['default_img'] = self.get_image_by_hash(image_hash)

        images = self.get_list_of_images(good)[:3]
        context['images'] = images
        context['positives'] = response['positives']
        context['negatives'] = response['negatives']
        context['points'] = response['points']
        context['categories'] = response['categories']
        context['comments'] = Comment.objects.filter(good=good)

        if request.user.is_authenticated:
            try:
                if Rate.objects.filter(Q(user=request.user) & Q(good=good)):
                    context['rated'] = str(
                        float('{:.2f}'.format(Rate.objects.filter(good=good).aggregate(Avg('rating'))['rating__avg'])))
            except Exception as exc:
                print(exc.args)
        else:
            try:
                if Rate.objects.filter(Q(good=good)):
                    context['rated'] = str(
                        float('{:.2f}'.format(Rate.objects.filter(good=good).aggregate(Avg('rating'))['rating__avg'])))
            except Exception as exc:
                print(exc.args)
        return render(request, self.template_name, context)
    
    
class GalleryPage(BaseView):
    template_name = 'photo/gallery.html'
    rated_previously = []

    def get_list_of_images(self, good_name):
        status_code, response = get_picture_list_by_good_name(good_name)
        data = []
        for image in response:
            data.append(image['file'])
        return data

    def get(self, request, good):
        context = {'name': good}
        if not request.user.is_authenticated:
            reg_form = UserRegistrationForm()
            context['reg_form'] = reg_form
        status_code, context['images'] = get_picture_list_by_good_name(good)
        return render(request, self.template_name, context)

    def post(self, request, good):
        context = {}
        if not request.user.is_authenticated:
            context['reg_form'], context['login_errors'] = self.check_auth(request)
        else:
            rate = request.POST.get('rate')
            image_id = request.POST.get('image_id')
            if rate and image_id:
                rate_photo = RatePhoto(
                    user=request.user,
                    image_id=image_id,
                    rating=rate
                )
                rate_photo.save()

        status_code, context['images'] = get_picture_list_by_good_name(good)

        return render(request, self.template_name, context)


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
                login(request, target_user, backend='django.contrib.auth.backends.ModelBackend')
                data_for_delete = Recovery.objects.filter(target_user=target_user)
                for item in data_for_delete:
                    item.delete()
                context['step'] = '4'
            else:
                context['step'] = '3'
                context['form'] = form
                context['error'] = 'Ошибка при заполнении полей'
    return render(request, 'registration/recovery_password.html', context)


def send_recovery_code(code, user):
    email_subject = 'EVILEG :: Сообщение через контактную форму '
    email_body = "Код для восстановления пароля: {}".format(code)
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['{}'.format(user.email)],
              fail_silently=False)


def profile(request):
    context = {'user': User.objects.get(id=request.user.id)}
    current_user = User.objects.get(id=request.user.id)
    context['comments'] = Comment.objects.filter(user=current_user)
    context['rates'] = Rate.objects.filter(user=request.user)
    context['own_goods'] = GoodsOnModeration.objects.filter(user=request.user)

    context['goods'] = requests.get('http://api.scanner.savink.in/api/v1/goods/all/',
                                    headers={'Authorization': '{}'.format(API_TOKEN)}).json()

    context['length'] = [i for i in range(len(context['goods']))]
    if UserPhoto.objects.filter(user=current_user):
        context['photo'] = UserPhoto.objects.get(user=current_user).img.url
    return render(request, 'profile/profile.html', context)


def change_info(request):
    current_user = User.objects.get(id=request.user.id)
    form = ChangeInfoForm(request.POST)
    form.fields['username'].widget.attrs['placeholder'] = current_user.username
    form.fields['email'].widget.attrs['placeholder'] = current_user.email
    photo = FileForm(request.POST, request.FILES)
    context = {'form': form, 'photo': photo}
    if UserPhoto.objects.filter(user=current_user):
        context['userphoto'] = UserPhoto.objects.get(user=current_user).img.url
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
            login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')
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


class AddUser(View):
    template_name = 'registration/add_user.html'

    def get(self, request):
        context = {'img': NotAuthUser.objects.get(id=request.GET.get('image')).file.url,
                   'user_form': UserRegistrationForm, 'image': NotAuthUser.objects.get(id=request.GET.get('image')).id}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        reg_form = UserRegistrationForm()
        errors = []
        if request.POST.get('status') == 'SignUp':
            reg_form = UserRegistrationForm(request.POST)
            if reg_form.is_valid():
                new_user = reg_form.save(commit=False)
                new_user.set_password(reg_form.cleaned_data['password2'])
                new_user.save()
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                good = GoodsOnModeration(
                    name=request.POST.get('name'),
                    image=NotAuthUser.objects.get(id=request.GET.get('image')).file,
                    user=new_user
                )
                response = requests.get('http://api.scanner.savink.in/api/v1/getbarcode/',
                                        files={'file': good.image.file},
                                        headers={'Authorization': '{}'.format(API_TOKEN)}
                                        ).json()

                if response['status'] == 'ok':
                    good.barcode = response['barcode']
                good.save()
                return redirect('/thanks/')
            else:
                context = {'img': NotAuthUser.objects.get(id=request.GET.get('image')).file.url,
                           'user_form': reg_form,
                           'image': NotAuthUser.objects.get(id=request.GET.get('image')).id,
                           'show_modal': False}
                return render(request, self.template_name, context)

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
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print('SingIn')
                picture = Picture(
                    user=user,
                    file=NotAuthUser.objects.get(id=request.GET.get('image')).file,
                )
                picture.save()
                return redirect(
                    to='/add_product/?image={}'.format(picture.id))
        context = {'img': NotAuthUser.objects.get(id=request.GET.get('image')).file.url,
                   'user_form': reg_form,
                   'image': NotAuthUser.objects.get(id=request.GET.get('image')).id,
                   'login_errors': errors,
                   'show_modal': True}
        return render(request, self.template_name, context)


class PhotoPage(TemplateView):
    context = {}
    context['modal_window'] = 'false'
    context['show_modal'] = 'false'
    context['main_image'] = ''
    template_name = 'photo/photo.html'

    def get(self, request):
        self.context['modal_window'] = 'false'
        form = BarcodeForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            auth = UserAuth(request, self.template_name)
            errors = auth.post()
            if errors:
                return render(self.request, self.template_name, errors)

        self.context['modal_window'] = False if request.POST.get('modal_check') == 'false' else True

        # Страница без модального окна
        if not self.context['modal_window']:
            form = BarcodeForm()
            self.context['form'] = form

            if not request.user.is_authenticated:
                self.context['show_modal'] = 'true'
                picture = NotAuthUser(
                    file=request.FILES['file'],
                    hash=imagehash.average_hash(Image.open(request.FILES['file']))
                )
                hashes_list = list(NotAuthUser.objects.values_list('hash', flat=True))
            else:
                picture = Picture(
                    user=request.user,
                    file=request.FILES['file'],
                    hash=imagehash.average_hash(Image.open(request.FILES['file']))
                )
                hashes_list = list(Picture.objects.values_list('hash', flat=True))
            hash_value = str(picture.hash)
            if hash_value not in hashes_list:
                picture.save()
                response = requests.get('http://api.scanner.savink.in/api/v1/goods/get_product/',
                                        files={'file': picture.file},
                                        params={'user': request.user.id,
                                                'platform': 'web'},
                                        headers={'Authorization': '{}'.format(API_TOKEN)}
                                        ).json()
                if not request.user.is_authenticated:
                    if response['status'] == 'ok':
                        return redirect(to='/product/{}/?image={}'.format(response['good'], picture.id))
                    else:
                        print('redirect')
                        return redirect(to='add_user/?image={}'.format(picture.id))
                else:
                    if response['status'] == 'ok':
                        return redirect(to='/product/{}/?image={}'.format(response['good'], picture.id))
                    else:
                        return redirect(to='/add_product/?image={}'.format(picture.id))
            else:
                if request.user.is_authenticated:
                    picture = Picture.objects.get(hash=hash_value)
                else:
                    picture = NotAuthUser.objects.get(hash=hash_value)
                if picture.target_good:
                    return redirect(to='/product/{}/?image={}'.format(str(picture.target_good), picture.id))
                else:
                    self.context['show_modal'] = 'true'

        # Страница с модальным окном
        else:
            self.context['modal_window'] = False
            form = BarcodeForm(request.POST)

            # Пользователь отправил новый файл
            if not ('barcode' in request.POST) or not (form.is_valid()):
                picture = Picture(
                    user=request.user,
                    file=request.FILES['file'],
                )
                picture.save()
                response = requests.get('http://api.scanner.savink.in/api/v1/goods/get_product/',
                                        files={'file': picture.file},
                                        params={'user': request.user.id,
                                                'platform': 'web'},
                                        headers={'Authorization': '{}'.format(API_TOKEN)}
                                        ).json()
                if response['status'] == 'ok':
                    return redirect(to='/product/{}/?image={}'.format(response['good'], picture.id))
                else:
                    return redirect(to='/add_product/?image={}'.format(picture.id))

            # Пользователь неверно ввёл баркод
            elif not form.is_valid():
                form = BarcodeForm()
                self.context['form'] = form
                self.context['form_errors'] = True

            # Пользователь корректно ввёл баркод
            else:
                good = GoodsOnModeration(
                    image=self.context['main_image'],
                    user=request.user,
                    barcode=request.POST.get('barcode')
                )
                response = requests.get('http://api.scanner.savink.in/api/v1/goods/barcode/{}/'.format(good.barcode),
                                        headers={'Authorization': '{}'.format(API_TOKEN)}
                                        ).json()

                # Обращение к api вызывает функцию класса GetByBarCode, которая не возвращает статус
                # if response['status'] == 'ok':
                #     good.name = response['name']

                if response:
                    good.name = response[0]['name']
                good.save()

                return redirect(to='/product/{}'.format(response[0]['name']))
        return render(request, self.template_name, self.context)


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
            category = request.POST.get('category')
            image = moderation_good.image

            if request.FILES:
                image = request.FILES.get('image')

            requests.post('http://api.scanner.savink.in/api/v1/goods/create/',
                          files={'file': image},
                          data={'user': request.user.id,
                                'name': name,
                                'category': category,
                                'barcode': barcode,
                                'points_rusControl': points
                                },
                          headers={'Authorization': '{}'.format(API_TOKEN)}
                          )
            moderation_good.status = 'Одобрено'
            moderation_good.save()

        elif request.POST.get('action') == 'deny':
            moderation_good = GoodsOnModeration.objects.get(id=request.POST.get('id'))
            moderation_good.status = 'Отклонено'
            moderation_good.save()

        elif request.POST.get('action') == 'create_category':
            payload = {}
            payload['name'] = request.POST.get('name')
            payload['url_name'] = request.POST.get('url_name')
            payload['parent'] = request.POST.get('category') or None
            image = request.FILES.get('image') or None

            requests.post('http://api.scanner.savink.in/api/v1/category/create/',
                          files={'file': image}, data=payload, headers=API_HEADERS)

        return render(request, self.template_name, self.get_context())

    def get_context(self):
        context = {}

        data_goods_on_moderation = GoodsOnModeration.objects.filter(status='Принято на модерацию')
        context['goods_data'] = data_goods_on_moderation

        categories = requests.get('http://api.scanner.savink.in/api/v1/category/all/',
                                  headers={'Authorization': '{}'.format(API_TOKEN)}
                                  ).json()
        context['categories'] = categories
        return context


class CategoryView(TemplateView):
    prev_category = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # Этот код для кнопки перехода "назад" работает только при последовательном переходе к товару
        # (в обратную сторону не работает, зацикливает переход)
        context['prev'] = '/category/' + CategoryView.prev_category
        CategoryView.prev_category = context['category']

        try:
            context['children'] = requests.get('http://api.scanner.savink.in/api/v1/category/filter/'
                                               '{}'.format(context['category']),
                                               headers={'Authorization': '{}'.format(API_TOKEN)}).json()
            context['goods'] = requests.get('http://api.scanner.savink.in/api/v1/goods/get_by_category/'
                                            '{}'.format(context['category']),
                                            headers={'Authorization': '{}'.format(API_TOKEN)}).json()
            data = context['goods']
            temporary = []
            for item in data:
                images = Picture.objects.filter(target_good=item['name']).distinct('target_good')
                temporary.append(images)
            context['images'] = temporary
            rate = []
            for item in data:
                rate.append(Rate.objects.filter(Q(good=item['name']) & Q(user=request.user)))
            print(rate)
            context['rated'] = rate

            if request.user.is_superuser:
                context['categories'] = requests.get('http://api.scanner.savink.in/api/v1/category/all/',
                                                     headers={'Authorization': '{}'.format(API_TOKEN)}).json()

                context['positives'] = requests.get('http://api.scanner.savink.in/api/v1/positive/all/',
                                                    headers={'Authorization': '{}'.format(API_TOKEN)}).json()

                context['negatives'] = requests.get('http://api.scanner.savink.in/api/v1/negative/all/',
                                                    headers={'Authorization': '{}'.format(API_TOKEN)}).json()

            return render(request, self.template_name, context)

        except ValueError:
            return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['prev'] = '/category/' + CategoryView.prev_category
        CategoryView.prev_category = context['category']
        payload = {}
        image = request.FILES.get('image')
        category_id = request.POST.get('category_id')

        if request.POST.get('type') == 'category':
            payload['name'] = request.POST.get('new_name')
            payload['url_name'] = request.POST.get('new_url')
            payload['parent'] = request.POST.get('parent')

            url = 'http://api.scanner.savink.in/api/v1/category/detail/{}/'.format(category_id)

            try:
                if request.POST.get('action') == 'category_delete':
                    requests.request("DELETE", url, headers=API_HEADERS)
                elif request.POST.get('action') == 'category_change':
                    requests.request("PUT", url, headers=API_HEADERS, data=payload, files={'file': image})
                elif request.POST.get('action') == 'add_good':
                    payload['category'] = request.POST.get('category_id')
                    payload['barcode'] = request.POST.get('barcode')
                    payload['points_rusControl'] = request.POST.get('points_rusControl')
                    requests.post('http://api.scanner.savink.in/api/v1/goods/create/',
                                  files={'file': image}, data=payload, headers=API_HEADERS)
                elif request.POST.get('action') == 'create_category':
                    payload['url_name'] = request.POST.get('url_name')
                    payload['parent'] = request.POST.get('parent') or None
                    image = request.FILES.get('image') or None
                    try:
                        requests.post('http://api.scanner.savink.in/api/v1/category/create/',
                                      files={'file': image}, data=payload, headers=API_HEADERS)
                    except ValueError:
                        return render(request, self.template_name, context)
            except ValueError:
                return render(request, self.template_name, context)

        elif request.POST.get('type') == 'good':
            good_id = request.POST.get('good_id')
            payload['name'] = request.POST.get('new_name')
            payload['barcode'] = request.POST.get('new_barcode')
            payload['points_rusControl'] = request.POST.get('new_points')
            payload['parent'] = request.POST.get('parent')
            url = 'http://api.scanner.savink.in/api/v1/goods/detail/{}/'.format(good_id)

            try:
                if request.POST.get('action') == 'delete':
                    requests.request("DELETE", url, headers=API_HEADERS)
                elif request.POST.get('action') == 'edit_good':
                    requests.request("PUT", url, headers=API_HEADERS, data=payload, files={'file': image})
            except ValueError:
                return render(request, self.template_name, context)

        elif request.POST.get('type') == 'positive':
            payload['value'] = request.POST.get('positive')
            payload['good'] = request.POST.get('good_id')

            positive_id = request.POST.get('positive_id')
            url = 'http://api.scanner.savink.in/api/v1/positive/detail/{}/'.format(positive_id)

            try:
                if request.POST.get('action') == 'add_positive':
                    requests.post('http://api.scanner.savink.in/api/v1/positive/create/',
                                  data=payload, headers=API_HEADERS)
                elif request.POST.get('action') == 'delete_positive':
                    requests.request("DELETE", url, headers=API_HEADERS)

            except ValueError:
                return render(request, self.template_name, context)

        elif request.POST.get('type') == 'negative':
            payload['value'] = request.POST.get('negative')
            payload['good'] = request.POST.get('good_id')

            negative_id = request.POST.get('negative_id')
            url = 'http://api.scanner.savink.in/api/v1/negative/detail/{}/'.format(negative_id)

            try:
                if request.POST.get('action') == 'add_negative':
                    requests.post('http://api.scanner.savink.in/api/v1/negative/create/',
                                  data=payload, headers=API_HEADERS)
                elif request.POST.get('action') == 'delete_negative':
                    requests.request("DELETE", url, headers=API_HEADERS)

            except ValueError:
                return render(request, self.template_name, context)

        context['categories'] = requests.get('http://api.scanner.savink.in/api/v1/category/all/',
                                             headers={'Authorization': '{}'.format(API_TOKEN)}).json()

        context['children'] = requests.get('http://api.scanner.savink.in/api/v1/category/filter/'
                                           '{}'.format(context['category']),
                                           headers={'Authorization': '{}'.format(API_TOKEN)}).json()

        context['goods'] = requests.get('http://api.scanner.savink.in/api/v1/goods/get_by_category/'
                                        '{}'.format(context['category']),
                                        headers={'Authorization': '{}'.format(API_TOKEN)}).json()

        context['positives'] = requests.get('http://api.scanner.savink.in/api/v1/positive/all/',
                                            headers={'Authorization': '{}'.format(API_TOKEN)}).json()

        context['negatives'] = requests.get('http://api.scanner.savink.in/api/v1/negative/all/',
                                            headers={'Authorization': '{}'.format(API_TOKEN)}).json()

        return render(request, self.template_name, context)


class CategoryFirstPageView(BaseTemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.is_authenticated:
            reg_form = UserRegistrationForm()
            context['reg_form'] = reg_form

        context['categories'] = requests.get('http://api.scanner.savink.in/api/v1/category/all/',
                                             headers={'Authorization': '{}'.format(API_TOKEN)}).json()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.is_authenticated:
            context['reg_form'], context['login_errors'] = self.check_auth(request)

        category_id = request.POST.get('category_id')

        payload = {}
        image = request.FILES.get('image')
        payload['name'] = request.POST.get('new_name')
        payload['url_name'] = request.POST.get('new_url')
        payload['parent'] = request.POST.get('parent')

        url = 'http://api.scanner.savink.in/api/v1/category/detail/{}/'.format(category_id)

        try:
            if request.POST.get('action') == 'category_delete':
                requests.request("DELETE", url, headers=API_HEADERS)
            elif request.POST.get('action') == 'category_change':
                requests.request("PUT", url, headers=API_HEADERS, data=payload, files={'file': image})
            elif request.POST.get('action') == 'add_good':
                payload['category'] = request.POST.get('category_id')
                payload['barcode'] = request.POST.get('barcode')
                payload['points_rusControl'] = request.POST.get('points_rusControl')
                requests.post('http://api.scanner.savink.in/api/v1/goods/create/',
                              files={'file': image}, data=payload, headers=API_HEADERS)
            elif request.POST.get('action') == 'create_category':
                payload['url_name'] = request.POST.get('url_name')
                payload['parent'] = request.POST.get('parent') or None
                image = request.FILES.get('image') or None
                try:
                    requests.post('http://api.scanner.savink.in/api/v1/category/create/',
                                  files={'file': image}, data=payload, headers=API_HEADERS)
                except ValueError:
                    return render(request, self.template_name, context)
        except ValueError:
            return render(request, self.template_name, context)

        context['categories'] = requests.get('http://api.scanner.savink.in/api/v1/category/all/',
                                             headers={'Authorization': '{}'.format(API_TOKEN)}).json()
        return render(request, self.template_name, context)


class AcceptPhotoPage(PermissionRequiredMixin, View):
    template_name = 'admin/photo_accept.html'
    permission_required = 'WEB_App.view'
    login_url = '/login/'

    def get(self, request):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request):
        picture_id = request.POST.get('picture_id')
        action = request.POST.get('action')
        try:
            picture_object = PictureOnModeration.objects.get(id=picture_id)
            if action == 'deny':
                picture_object.status = 'Отклонено'
                picture_object.save()
            elif action == 'accept':
                picture_object.status = 'Одобрено'
                picture_object.save()
                new_picture = Picture(file=picture_object.image,
                                      user=picture_object.user,
                                      target_good=picture_object.target_good,
                                      hash=imagehash.average_hash(Image.open(request.FILES['file']))
                                      )
                new_picture.save()
        except Exception:
            return render(request, '500.html')

        context = self.get_context()
        return render(request, self.template_name, context)

    def get_context(self):
        context = {'photo_data': PictureOnModeration.objects.filter(status='Принято на модерацию')}
        return context
