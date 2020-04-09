"""Scanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from WEB_App.views import *


urlpatterns = [
    path('', index),
    path('registration/', signup),
    path('recovery_password/', recovery_password),
    path('photo/', login_required(PhotoPage.as_view())),
    path('product/<str:good>/', ProductPage.as_view()),
    path('gallery/<str:good>', GalleryPage.as_view()),
    path('add_product/', login_required(AddProductPage.as_view())),
    path('thanks/', TemplateView.as_view(template_name='photo/thanks.html')),
    path('admin/accept/', AcceptPage.as_view()),
    path('admin/accept_photo/', AcceptPhotoPage.as_view()),
    path('admin/urls/', TemplateView.as_view(template_name='admin/links.html')),
    path('profile/', profile),
    path('change_info/', change_info),

    path('category/<str:category>', CategoryView.as_view(template_name='categories/category_list.html')),
    path('category/', CategoryFirstPageView.as_view(template_name='categories/category_first_list.html')),
]