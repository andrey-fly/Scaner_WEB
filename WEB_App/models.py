"""
Самописные классы для Django с целью создания моделей для базы данных
"""
from django.contrib.auth.models import User
from django.db import models


class Recovery(models.Model):
    """
    Класс для таблицы восстановления пароля в базе данных. Поля: target_user(пользователь, \
    восстанавливающий пароль), from_ip(ip пользователя), code(код для восстановления), \
    created(дата создания). Отнаследован от базового класса Django models.Model
    """
    target_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    from_ip = models.CharField(max_length=15, null=False, default=None)
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


class UserPhoto(models.Model):
    """
    Класс для аватаров пользователей. Поля: user(пользователь), img(ссылка на файл аватара в S3 \
    хранилище), created(дата создания), updated(дата изменения). Отнаследован от базового класса \
    Django models.Model
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profile_photos', null=True, default='profile_icon')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)


class GoodsOnModeration(models.Model):
    """
    Класс для товаров на модерации. Поля: name(наименование товара), image(ссылка на файл \
    картинки в S3 хранилище), barcode(штрих-код товара), STATUSES(все статусы), status(текущий \
    статус модерации), user(пользователь, добавивший товар), created(дата создания). \
    Отнаследован от базового класса Django models.Model
    """
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
    """
    Класс для хранения ссылок и хэшей картинок. Поля: file(ссылка на файл картинки в S3 \
    хранилище), hash(хэш картинки), user(пользователь, загрузивший фото), created(дата \
    создания), target_good(товар, которому принадлежит фото). Отнаследован от базового класса \
    Django models.Model
    """
    file = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    hash = models.TextField(verbose_name='Хэш фото', null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE,
                             null=True, default=None)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    target_good = models.TextField(verbose_name='Товар', null=True)
    # platform = models.TextField(verbose_name='Платформа', default='Неизвестная платформа')


class PictureOnModeration(models.Model):
    """
    Класс для хранения картинок на ммодерации. Поля: image(ссылка на файл картинки в S3 \
    хранилище), target_good(товар, которому принадлежит картинка), STATUSES(все статусы), \
    status(текущий статус), user(пользователь, загрузивший фото), created(дата создания). \
    Отнаследован от базового класса Django models.Model
    """
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
    """
    Класс для хранения комментариев. Поля: text(текст комментария), user(пользователь, \
    оставивший комментарий), created(дата создание), good(прокомментированный товар). \
    Отнаследован от базового класса Django models.Model
    """
    text = models.TextField(verbose_name='Содержимое комментария', null=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)
    good = models.TextField(verbose_name='Товар')

    def get_children(self):
        """
        Функция для получения ответов на родительский комментарий

        :return: Объект типа ChildrenComment
        """
        return ChildrenComment.objects.filter(parent=self)


class ChildrenComment(models.Model):
    """
    Класс для хранения ответов на комментарии. Поля: text(текст ответа на комментарий), \
    user(пользователь, оставивший ответ на комментарий), parent(родительский комментарий), \
    created(дата создания). Отнаследован от базового класса Django models.Model
    """
    text = models.TextField(verbose_name='Содержимое комментария', null=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    parent = models.ForeignKey(Comment, verbose_name='Комментарий', null=False,
                               on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)


class Rate(models.Model):
    """
    Класс для хранения оценок товара. Поля: user(пользователь, оценивший товар), rating(оценка),\
    good(оценненый това), created(дата создания). Отнаследован от базового класса Django
    models.Model
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rating = models.FloatField(verbose_name='Рейтинг')
    good = models.TextField(verbose_name='Товар')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)


class RatePhoto(models.Model):
    """
    Класс для хранения оценок фотографии товара. Поля: user(пользователь, оценивший товар), \
    image_id(id оцененной картинки), rating(оценка), created(дата создания). Отнаследован от \
    базового класса Django models.Model
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    image_id = models.IntegerField(verbose_name='image ID')
    rating = models.FloatField(verbose_name='Рейтинг')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)


class NotAuthUser(models.Model):
    """
    Класс для добавления товара неавторизованным пользователем. Поля: file(ссылка на файл \
    фотографии в S3 хранилище), created(дата создания), target_good(товар, которому принадлежит \
    фото), hash(хэш фотографии). Отнаследован от базового класса Django models.Model
    """
    file = models.ImageField(verbose_name='Ссылка на s3 хранилище', upload_to='photos')
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=False)
    target_good = models.TextField(verbose_name='Товар', null=True)
    hash = models.TextField(verbose_name='Хэш фото', null=True)


class Complaint(models.Model):
    """
    Класс хранения контактов пользователя с администрацией. Поля: user(пользователь, написавший \
    сообщение), date(дата создания), title(заголовок сообщения), text(текст сообщения), \
    checked(Проверено ли сообщение). Отнаследован от базового класса Django models.Model
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата отправки', auto_now_add=True, null=False)
    title = models.CharField(verbose_name='Заголовок жалобы', max_length=255, null=False)
    text = models.TextField(verbose_name='Содержимое жалобы', null=False)
    checked = models.BooleanField(verbose_name='Проверено ли', default=False)


class ComplaintResponse(models.Model):
    """
    Класс для ответа пользователю. Поля: user(модератор, отвечающий на сообщение), date(дата \
    создания), parent(исходное сообщение), title(заголовок сообшения), text(текст сообщения), \
    checked(прочитано ли сообщение). Отнаследован от базового класса Django models.Model
    """
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата отправки ответа', auto_now_add=True, null=False)
    parent = models.ForeignKey(Complaint, verbose_name='Жалоба', null=False,
                               on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок жалобы', max_length=255, null=False)
    text = models.TextField(verbose_name='Содержимое ответа на жалобу', null=False)
    checked = models.BooleanField(verbose_name='Прочитано ли', default=False)
