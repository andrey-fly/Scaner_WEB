from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

class Recovery(models.Model):
    target_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_ip = models.CharField(max_length=15, null=False, default=None)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


class UserPhoto(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profile', null=True, default='profile_icon')


class GoodsOnModeration(models.Model):
    name = models.TextField(verbose_name='Наименование', max_length=255)
    image = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos', null=True)
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


class Picture(models.Model):
    file = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    target_good = models.TextField(verbose_name='Товар', null=True)
    # platform = models.TextField(verbose_name='Платформа', default='Неизвестная платформа')


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


class RatePhoto(models.Model):
    RATE = ((1, _("Ужасно")),
            (2, _("Плохо")),
            (3, _("Нормально")),
            (4, _("Хорошо")),
            (5, _("Отлично"))
            )
    rate = models.IntegerField(choices=RATE,
                               default=1)
    parent = models.ForeignKey(Picture, verbose_name='Фото', null=False, on_delete=models.CASCADE)
