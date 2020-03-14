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
from django.contrib import admin
from django.urls import path, include

from API_App.views import GoodsCreateView, GoodsListView, GoodsDetailView, GetByBarCode, SearchProduct, \
    CategoryCreateView, CategoryListView, CategoryDetailView, PictureCreateView, PictureListView, PictureDetailView, \
    NegativeCreateView, NegativeListView, NegativeDetailView, PositiveCreateView, PositiveDetailView, PositiveListView, \
    GetBarCode

urlpatterns = [
    path('goods/create/', GoodsCreateView.as_view()),
    path('goods/all/', GoodsListView.as_view()),
    path('goods/detail/<int:pk>/', GoodsDetailView.as_view()),

    path('category/create/', CategoryCreateView.as_view()),
    path('category/all/', CategoryListView.as_view()),
    path('category/detail/<int:pk>/', CategoryDetailView.as_view()),

    path('picture/create/', PictureCreateView.as_view()),
    path('picture/all/', PictureListView.as_view()),
    path('picture/detail/<int:pk>/', PictureDetailView.as_view()),

    path('negative/create/', NegativeCreateView.as_view()),
    path('negative/all/', NegativeListView.as_view()),
    path('negative/detail/<int:pk>/', NegativeDetailView.as_view()),

    path('positive/create/', PositiveCreateView.as_view()),
    path('positive/all/', PositiveListView.as_view()),
    path('positive/detail/<int:pk>/', PositiveDetailView.as_view()),

    path('goods/barcode/<str:barcode>/', GetByBarCode.as_view()),
    path('goods/get_product/', SearchProduct.as_view()),

    path('getbarcode/', GetBarCode.as_view())
]
