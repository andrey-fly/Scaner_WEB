from rest_framework import serializers

from API_App.models import Goods


class GoodsDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goods
        fields = '__all__'
        # fields = ('id', 'name', 'user')


class GoodsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'