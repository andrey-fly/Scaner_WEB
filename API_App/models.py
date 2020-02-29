from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class Goods(models.Model):
    name = models.CharField(verbose_name='Наименование', db_index=True, max_length=128)
    barcode = models.CharField(verbose_name='Штрих-код', db_index=True, max_length=12, default=None, null=True)
    imageAIname = models.CharField(verbose_name='Имя в модели нейросети', db_index=True, max_length=64, default=None, null=True)
    CATEGORIES = (
        (1, 'Молочные продукты'),
        (2, 'Мясные продукты'),
    )
    category = models.IntegerField(verbose_name='Категория', choices=CATEGORIES, default=None, null=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

class Picture(models.Model):
    s3_link = models.CharField(verbose_name='Ссылка на s3 хранилище', max_length=255)

    file = models.FileField(upload_to='photos')
    #width =models.IntegerField()
    #height = models.IntegerField()
    #good = models.ForeignKey(to=Goods,on_delete=models.CASCADE)

