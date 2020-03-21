from django.contrib.auth.models import User
from django.db import models

from API_App.models import Picture


class Recovery(models.Model):
    target_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_ip = models.CharField(max_length=15, null=False, default=None)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


class GoodsOnModeration(models.Model):
    name = models.TextField(verbose_name='Наименование', max_length=255)
    image = models.ForeignKey(Picture, verbose_name='Изображение', on_delete=models.CASCADE)
    barcode = models.TextField(verbose_name='Штрих-код', db_index=True, default=None, null=True)
    STATUSES = [
        (1, 'Принято на модерацию'),
        (2, 'Обработано'),
        (3, 'Отклонено'),
    ]
    status = models.CharField(verbose_name='Статус', max_length=25,
                              choices=STATUSES, default=1)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class UserPhoto(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profile', null=True, default='profile_icon')
