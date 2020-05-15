"""
Базовые классы, от которых наследуются классы в WEB_App.view
"""
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from WEB_App.forms import UserRegistrationForm


class UserAuth:
    """
    Базовый класс аутентификации пользователя. Используется для регистрации/аутентификации на \
    всех страницах сайт. Конструктор принимает на вход request(Django-feature) и имя шаблона \
    страницы
    """

    def __init__(self, request, template_name):
        """
        Конструктор класса UserAuth

        :param request: Обязательный параметр для класса в Django
        :param template_name: Имя шаблона страницы
        """
        self.template_name = template_name
        self.request = request
        self.reg_form = UserRegistrationForm()
        self.errors = []

    def sign_up(self):
        """
        Функция для регистрации пользователя на сайте

        :return: None
        """
        new_user = self.reg_form.save(commit=False)
        new_user.set_password(self.reg_form.cleaned_data['password2'])
        new_user.save()
        login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')

    def sign_in(self):
        """
        Функция для авторизации пользователя на сайте

        :return: None
        """
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
        """
        Функция для определения действия пользователя: авторизация или регистрация

        :return: Форма регистрации и ошибки при регистрации, если они есть
        """
        if self.request.POST.get('status') == 'SignUp':
            self.reg_form = UserRegistrationForm(self.request.POST)
            if self.reg_form.is_valid():
                self.sign_up()
        elif self.request.POST.get('status') == 'SignIn':
            self.sign_in()
        return self.reg_form, self.errors


class BaseView(View):
    """
    Базовый класс для View-классов. Отнаследован от стандартного класса Django(View)
    """
    template_name = 'main/index.html'

    def get(self, request):
        """
        Функция, обрабатывающая get-запросы страниц

        :param request: Обязательный парпметр Django-классов
        :return: Запросы к старнице, шаблон старницы, а так же передаваемый контекст \
        для рендера страницы в html формат. Стандартный return в Django-функции
        """
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Функция, обрабатывающая post-запросы страниц

        :param request: Обязательный парпметр Django-классов
        :return: Запросы к старнице, шаблон старницы, а так же передаваемый контекст \
        для рендера страницы в html формат. Стандартный return в Django-функции
        """
        context = {}
        return render(request, self.template_name, context)

    def check_auth(self, request):
        """
        Функция решистрации/авторизации пользователя на сайте. Вызывает метод из класса UserAuth

        :param request: Обязательный парпметр Django-классов
        :return: Вызов метода регистрации/авторизации из класса UserAuth
        """
        auth = UserAuth(request, self.template_name)
        return auth.check_auth()


class BaseTemplateView(TemplateView):
    """
    Базовый класс для TemplateView-классов. Отнаследован от стандартного класса Django TemolateView
    """
    def get(self, request, *args, **kwargs):
        """
        Функция, обрабатывающая get-запросы страниц

        :param request: Обязательный парпметр Django-классов
        :param args: Автоматический параметр для заполнения сontext
        :param kwargs: Автоматический параметр для заполнения сontext
        :return: Запросы к старнице, шаблон старницы, а так же передаваемый контекст \
        для рендера страницы в html формат. Стандартный return в Django-функции
        """
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Функция, обрабатывающая post-запросы страниц

        :param request: Обязательный парпметр Django-классов
        :return: Запросы к старнице, шаблон старницы, а так же передаваемый контекст \
        для рендера страницы в html формат. Стандартный return в Django-функции
        """
        context = {}
        return render(request, self.template_name, context)

    def check_auth(self, request):
        """
        Функция решистрации/авторизации пользователя на сайте. Вызывает метод из класса
        UserAuth

        :param request: Обязательный парпметр Django-классов
        :return: Вызов метода регистрации/авторизации из класса UserAuth
        """
        auth = UserAuth(request, self.template_name)
        return auth.check_auth()
