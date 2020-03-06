from rest_framework import serializers

from API_App.models import Goods, Picture, Category, Positive, Negative


class DetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = None
        field = '__all__'


class ListSerializer(serializers.ModelSerializer):
    pass


# For goods
class GoodsDetailSerializer(DetailSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class GoodsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


#  for pictures
class PictureDetailSerializer(DetailSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class PictureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'


# for categories
class CategoryDetailSerializer(DetailSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# for positive characteristics
class PositiveDetailSerializer(DetailSerializer):
    class Meta:
        model = Positive
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class PositiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positive
        fields = '__all__'


# for negative characteristics
class NegativeDetailSerializer(DetailSerializer):
    class Meta:
        model = Negative
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class NegativeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negative
        fields = '__all__'