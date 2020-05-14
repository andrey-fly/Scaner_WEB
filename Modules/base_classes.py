from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from WEB_App.forms import UserRegistrationForm


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