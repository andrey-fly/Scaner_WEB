from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Наименование', db_index=True, max_length=128)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)

    def get_choices(self):
        data = Category.objects.all()
        choices = []
        for item in data:
            choices.append((item.id, '{}'.format(item.name)))
        return choices


class Goods(models.Model):
    name = models.CharField(verbose_name='Наименование', db_index=True, max_length=128)
    barcode = models.CharField(verbose_name='Штрих-код', db_index=True, max_length=12, default=None, null=True)
    imageAIname = models.CharField(verbose_name='Имя в модели нейросети', db_index=True, max_length=64, default=None, null=True)
    CATEGORIES = [
        (1, 'Молочные продукты'),
        (2, 'Мясные продукты'),
    ]
    category = models.IntegerField(verbose_name='Категория', choices=CATEGORIES, default=None, null=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)


class Picture(models.Model):
    file = models.FileField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)


class Positive(models.Model):
    goods = models.ForeignKey(to=Goods, verbose_name='Продукт', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Достоинство', max_length=128)


class Negative(models.Model):
    goods = models.ForeignKey(to=Goods, verbose_name='Продукт', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Недостаток', max_length=128)




