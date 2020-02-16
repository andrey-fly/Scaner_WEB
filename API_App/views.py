from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from API_App.models import Goods
from API_App.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from API_App.serializer import GoodsDetailSerializer, GoodsListSerializer


class GoodsCreateView(generics.CreateAPIView):
    serializer_class = GoodsDetailSerializer
    permission_classes = (IsAdminUser, )


class GoodsListView(generics.ListAPIView):
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.all()
    permission_classes = (IsAuthenticated, )


class GoodsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoodsDetailSerializer
    queryset = Goods.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsOwnerOrReadOnly, IsAdminUser)
