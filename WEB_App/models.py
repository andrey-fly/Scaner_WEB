from django.contrib.auth.models import User
from django.db import models


class Recovery(models.Model):
    target_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_ip = models.CharField(max_length=15, null=False, default=None)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


class UserPhoto(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profile_photos', null=True, default='profile_icon')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)


class GoodsOnModeration(models.Model):
    name = models.TextField(verbose_name='Наименование', max_length=255)
    image = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)
    barcode = models.TextField(verbose_name='Штрих-код', db_index=True, default=None, null=True)
    STATUSES = [
        (1, 'Принято на модерацию'),
        (2, 'Одобрено'),
        (3, 'Отклонено'),
    ]
    status = models.CharField(verbose_name='Статус', max_length=25,
                              choices=STATUSES, default='Принято на модерацию')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Picture(models.Model):
    file = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    hash = models.TextField(verbose_name='Хэш фото', null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, default=None)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    target_good = models.TextField(verbose_name='Товар', null=True)
    # platform = models.TextField(verbose_name='Платформа', default='Неизвестная платформа')


class PictureOnModeration(models.Model):
    image = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)
    target_good = models.TextField(verbose_name='Товар', null=True)
    STATUSES = [
        (1, 'Принято на модерацию'),
        (2, 'Одобрено'),
        (3, 'Отклонено'),
    ]
    status = models.CharField(verbose_name='Статус', max_length=25,
                              choices=STATUSES, default='Принято на модерацию')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(verbose_name='Содержимое комментария', null=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)
    good = models.TextField(verbose_name='Товар')

    def get_children(self):
        return ChildrenComment.objects.filter(parent=self)


class ChildrenComment(models.Model):
    text = models.TextField(verbose_name='Содержимое комментария', null=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    parent = models.ForeignKey(Comment, verbose_name='Комментарий', null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)


class Rate(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rating = models.FloatField(verbose_name='Рейтинг')
    good = models.TextField(verbose_name='Товар')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)


class RatePhoto(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    image_id = models.IntegerField(verbose_name='image ID')
    rating = models.FloatField(verbose_name='Рейтинг')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)


class NotAuthUser(models.Model):
    file = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)
    target_good = models.TextField(verbose_name='Товар', null=True)
    hash = models.TextField(verbose_name='Хэш фото', null=True)


class Complaint(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата отправки', auto_now_add=True, null=False)
    title = models.CharField(verbose_name='Заголовок жалобы', max_length=255, null=False)
    text = models.TextField(verbose_name='Содержимое жалобы', null=False)
    checked = models.BooleanField(verbose_name='Проверено ли', default=False)


class ComplaintResponse(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата отправки ответа', auto_now_add=True, null=False)
    parent = models.ForeignKey(Complaint, verbose_name='Жалоба', null=False, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок жалобы', max_length=255, null=False)
    text = models.TextField(verbose_name='Содержимое ответа на жалобу', null=False)
    checked = models.BooleanField(verbose_name='Прочитано ли', default=False)
