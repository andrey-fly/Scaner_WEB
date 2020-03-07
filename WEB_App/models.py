from django.contrib.auth.models import User
from django.db import models

from API_App.models import Picture


class Recovery(models.Model):
    target_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_ip = models.CharField(max_length=15, null=False, default=None)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


class GoodsInModeration(models.Model):
    name = models.TextField(verbose_name='Наименование', max_length=255)
    image = models.ForeignKey(Picture, verbose_name='Изображение', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)