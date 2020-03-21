from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(verbose_name='Наименование', max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['name']
        parent_attr = 'parent'
        left_attr = 'lft'
        right_attr = 'rght'
        tree_id_attr = 'tree_id'
        order_insertion_by = []


class Goods(models.Model):
    name = models.CharField(verbose_name='Наименование', db_index=True, max_length=128, unique=True)
    barcode = models.TextField(verbose_name='Штрих-код', db_index=True, default=None, null=True)
    imageAIname = models.CharField(verbose_name='Имя в модели нейросети', db_index=True,
                                   max_length=64, default=None, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, default=None, null=True)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)
    points_rusControl = models.CharField(verbose_name='Оценка Росконтроля',
                                         max_length=10, default='Не указано', null=True)

    def get_positives(self):
        return Positive.objects.filter(good=self)

    def get_negatives(self):
        return Negative.objects.filter(good=self)

    def get_comments(self):
        return Comment.objects.filter(good=self)


class Picture(models.Model):
    file = models.FileField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    # user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    target_good = models.ForeignKey(Goods, verbose_name='Товар', on_delete=models.CASCADE, null=True, default=None)
    platform = models.TextField(verbose_name='Платформа', default='Неизвестная платформа')


class Positive(models.Model):
    good = models.ForeignKey(to=Goods, verbose_name='Продукт', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Достоинство', max_length=128)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)


class Negative(models.Model):
    good = models.ForeignKey(to=Goods, verbose_name='Продукт', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Недостаток', max_length=128)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария", max_length=255)
    good = models.ForeignKey(to=Goods, verbose_name='Продукт', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# class UserActions(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
#     status = models.BooleanField(verbose_name='Успех')
#     target_good = models.ForeignKey(Goods, verbose_name='Товар', on_delete=models.CASCADE, null=True, default=None)
#     uploaded_image = models.ForeignKey(Picture, verbose_name='Загруженное изображение', on_delete=models.CASCADE, null=True, default=None)



