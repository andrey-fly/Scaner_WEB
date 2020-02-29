from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from API_App.models import Goods
from API_App.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from API_App.serializer import GoodsDetailSerializer, GoodsListSerializer
from Modules.ImageController import ImageController


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


class GetByBarCode(generics.ListAPIView):
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.none()
    permission_classes = ()

    def get(self, request, barcode):
        queryset = Goods.objects.filter(barcode=barcode)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


from pyzbar import pyzbar
import cv2
class SearchProduct(generics.ListAPIView):
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.none()
    permission_classes = ()

    def get(self, request):
        queryset = []
        serializer = self.serializer_class(queryset, many=True)

        print('----API----')
        print(request.GET)
        print(request.FILES)
        print('-----------')

        # ПОЛУЧЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ
        image_controller = ImageController()
        # СОХРАНЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ
        image_controller.save(request_file=request.FILES['file'])

        # ИЩЕМ БАРКОД
        image = cv2.imread('collectedmedia/{}'.format(image_controller.get_file_name()))
        barcodes = pyzbar.decode(image)
        print(barcodes)
        for barcode in barcodes:
            print(barcode.data.decode('ascii'))

        return Response(serializer.data)