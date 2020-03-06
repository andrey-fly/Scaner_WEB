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


# base rest views classes
class BaseCreateView(generics.CreateAPIView):
    serializer_class = None
    permission_classes = (IsAdminUser, )


class BaseListView(generics.ListAPIView):
    serializer_class = None
    queryset = []
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )


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
    queryset = Goods.objects.none()
    permission_classes = ()

    def get(self, request):
        # ПОЛУЧЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ
        image_controller = ImageController()
        # СОХРАНЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ
        image_controller.save(request_file=request.FILES['file'])

        # ИЩЕМ БАРКОД
        barcode_detector = BarcodeDetector()
        bar = barcode_detector.detect('collectedmedia/{}'.format(image_controller.get_file_name()))
        # print(bar[0]['barcode'])
        # print(bar[0]['rect'])
        # print(bar[0]['rect']['x'])

        # УДАЛЕНИЕ КАРТИНКИ ПОЛЬЗОВАТЕЛЯ
        image_controller.delete_image()

        self.queryset = bar
        # print(self.queryset)
        return Response(self.queryset)
