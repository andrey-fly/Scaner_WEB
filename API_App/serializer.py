from rest_framework import serializers

from API_App.models import Goods, Picture, Category, Positive, Negative


class BaseDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class BaseListSerializer(serializers.ModelSerializer):
    pass


# For goods
class GoodsDetailSerializer(BaseDetailSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class GoodsListSerializer(BaseListSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


#  for pictures
class PictureDetailSerializer(BaseDetailSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class PictureListSerializer(BaseListSerializer):
    class Meta:
        model = Picture
        fields = '__all__'


# for categories
class CategoryDetailSerializer(BaseDetailSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class CategoryListSerializer(BaseListSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# for positive characteristics
class PositiveDetailSerializer(BaseDetailSerializer):
    class Meta:
        model = Positive
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class PositiveListSerializer(BaseListSerializer):
    class Meta:
        model = Positive
        fields = '__all__'


# for negative characteristics
class NegativeDetailSerializer(BaseDetailSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Negative
        fields = '__all__'
        # fields = ('goods', 'value')

    def create(self, validated_data):
        return Negative.objects.create(**validated_data)


class NegativeListSerializer(BaseListSerializer):
    class Meta:
        model = Negative
        fields = '__all__'