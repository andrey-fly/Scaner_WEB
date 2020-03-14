from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from API_App.models import Goods, Category, Picture, Negative, Positive
from API_App.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from API_App.serializer import GoodsDetailSerializer, GoodsListSerializer, CategoryDetailSerializer, \
    CategoryListSerializer, PictureDetailSerializer, PictureListSerializer, NegativeDetailSerializer, \
    NegativeListSerializer, PositiveDetailSerializer, PositiveListSerializer
from Modules.BarcodeDetector import BarcodeDetector
from Modules.ImageController import ImageController

from django.contrib.auth.models import User


# base rest views classes
class BaseCreateView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (IsAdminUser,)


class BaseListView(generics.ListAPIView):
    serializer_class = None
    queryset = []
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class BaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = None
    queryset = []
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsOwnerOrReadOnly, IsAdminUser)


# goods rest view classes
class GoodsCreateView(BaseCreateView):
    serializer_class = GoodsDetailSerializer


class GoodsListView(BaseListView):
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.all()


class GoodsDetailView(BaseDetailView):
    serializer_class = GoodsDetailSerializer
    queryset = Goods.objects.all()


# category rest view classes
class CategoryCreateView(BaseCreateView):
    serializer_class = CategoryDetailSerializer


class CategoryListView(BaseListView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class CategoryDetailView(BaseDetailView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()


# pictures rest view classes
class PictureCreateView(BaseCreateView):
    serializer_class = PictureDetailSerializer


class PictureListView(BaseListView):
    serializer_class = PictureListSerializer
    queryset = Picture.objects.all()


class PictureDetailView(BaseDetailView):
    serializer_class = PictureDetailSerializer
    queryset = Picture.objects.all()


# negative characteristics rest view classes
class NegativeCreateView(BaseCreateView):
    serializer_class = NegativeDetailSerializer


class NegativeListView(BaseListView):
    serializer_class = NegativeListSerializer
    queryset = Negative.objects.all()


class NegativeDetailView(BaseDetailView):
    serializer_class = NegativeDetailSerializer
    queryset = Negative.objects.all()


# positive characteristics rest view classes
class PositiveCreateView(BaseCreateView):
    serializer_class = PositiveDetailSerializer


class PositiveListView(BaseListView):
    serializer_class = PositiveListSerializer
    queryset = Positive.objects.all()


class PositiveDetailView(BaseDetailView):
    serializer_class = PositiveDetailSerializer
    queryset = Positive.objects.all()


# any
class GetByBarCode(generics.ListAPIView):
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.none()
    permission_classes = ()

    def get(self, request, barcode):
        queryset = Goods.objects.filter(barcode=barcode)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class SearchProduct(generics.ListAPIView):
    serializer_class = GoodsListSerializer
    queryset = Goods.objects.all()
    permission_classes = ()

    def get(self, request):
        queryset = {'status': None}
        # ПОЛУЧЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ
        image_controller = ImageController()
        # СОХРАНЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ ДЛЯ ОБРАБОТКИ
        image_controller.save(request_file=request.FILES['file'])

        # ИЩЕМ БАРКОД
        barcode_detector = BarcodeDetector()
        bar = barcode_detector.detect('collectedmedia/{}'.format(image_controller.get_file_name()))

        target_good = None

        picture = Picture(file=request.FILES['file'],
                          platform=request.GET.get('platform'))

        if bar and Goods.objects.filter(barcode=bar[0]['barcode']):
            target_good = Goods.objects.get(barcode=bar[0]['barcode'])
            picture.target_good = target_good

            positives_q = Positive.objects.filter(good=target_good)
            negatives_q = Negative.objects.filter(good=target_good)
            positives = []
            negatives = []
            for item in positives_q:
                positives.append(item.value)
            for item in negatives_q:
                negatives.append(item.value)

            queryset['status'] = 'ok'
            queryset['good'] = target_good.name

            # queryset['positives'] = positives
            # queryset['negatives'] = negatives

        # УДАЛЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ ПОСЛЕ ОБРАБОТКИ
        image_controller.delete_image()

        picture.save()
        queryset['image'] = picture.id

        return Response(queryset)


class GetBarCode(generics.ListAPIView):
    serializer_class = None
    queryset = None
    permission_classes = ()

    def get(self, request):
        queryset = {'status': None}
        image_controller = ImageController()
        barcode_detector = BarcodeDetector()

        image_controller.save(request_file=request.FILES['file'])
        bar = barcode_detector.detect('collectedmedia/{}'.format(image_controller.get_file_name()))

        if bar:
            bar = bar[0]['barcode']

            queryset['status'] = 'ok'
            queryset['barcode'] = bar

        image_controller.delete_image()

        return Response(queryset)