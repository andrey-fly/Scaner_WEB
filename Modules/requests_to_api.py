"""
Модуль запросов к API. Используется для связи WEB и API интерфейсов
"""
import requests

from Scanner.settings import API_HEADERS


def get_product(image, author):
    """
    Получение продукта по картинке с сервера API. Используется при загрузке фото пользователем \
    для поиска товара по картинке

    :param image: Файл с картинкой для поиска в базе данных
    :param author: Автор запроса(пользователь, загрузивший фото)
    :return: Статус запроса и данные(статус, название товара и способ распознования), переданные \
    с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods/get_product/'
    params = {'platform': 'WEB', 'author': author}
    response = requests.request("GET", url, headers=API_HEADERS, params=params,
                                files={'file': image})
    return response.status_code, response.json()


def get_picture_by_hash(own_hash):
    """
    Получение продукта по хэшу картинки с сервера API. Передача картинки через её хэш для \
    отображение на странице товара и добавлении товара

    :param own_hash: Файл картинки для преобразования в хэш на API
    :return: Статус запроса и данные(статус, объект Picture), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/picture/get_picture_by_hash/{}'.format(own_hash)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_picture_by_id(own_id):
    """
    Получение картинки по id с сервера API. Используется для отображение картинок на модерации

    :param own_id: Id картинки на сервере
    :return: Статус запроса и данные(статус, объект Picture), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/picture/detail/{}'.format(own_id)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def download_by_hash(own_hash):
    """
    Передача файла с API на WEB. Загрузка картинки для отображения на странице добаления товара

    :param own_hash: Картинка для хэширования на API
    :return: url файла в S3 хранилище
    """
    url = 'http://api.scanner.savink.in/api/v1/picture/download_picture_by_hash/{}'.format(
        own_hash)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response


def create_moderation_good_with_hash(own_hash, name, barcode):
    """
    Создание товара на модерацию с отправкой файла для хэширования на API. Используется на \
    странице добаления товара для создания товара в панели модерации

    :param own_hash: Файл для хэширования на API
    :param name: Название товара
    :param barcode: Баркод товара
    :return: Статус запроса и данные(статуст, объект GoodsOnModeration), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods_on_moderation/create_by_hash/'
    payload = {'name': name, 'barcode': barcode, 'hash': own_hash}
    response = requests.request("POST", url, data=payload, headers=API_HEADERS)
    return response.status_code, response.json()


def get_barcode(image):
    """
    Полуение штих-кода товара с API. Используется на странице добавления товара для получения \
    баркода с картинки

    :param image: Файл загруженной картинки
    :return: Баркод товара
    """
    url = 'http://api.scanner.savink.in/api/v1/getbarcode/'
    response = requests.request("GET", url, headers=API_HEADERS, files={'file': image}).json()
    barcode = None
    if response['status'] == 'ok':
        barcode = response['barcode']
    return barcode


def get_good_by_name(good):
    """
    Получение товара по имени с сервера API. Используется на странице товара для отображения \
    стандартного изображения товара, заданного администраторами

    :param good: Название товара
    :return: Статус запроса и данные(статус, объект Good), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods/get_by_name/{}/'.format(good)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_picture_list_by_good_name(good_name):
    """
    Получение списка всех фото товара из API по имени этого товара. Используется на странице \
    галереи для отображения всех фото товара

    :param good_name: Название товара, со страницы которого производился переход  в галерею
    :return: Статус запроса и данные(статус, объект Picture), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/picture/get_pictures_list_by_good_name/{}'.format(
        good_name)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_moderation_goods_by_status(status):
    """
    Получение всех товаров на модерации по их статусу. Используется в панеле администратора

    :param status: Статус товара на модерации('Принято на модерацию, одобрено или отклонено)
    :return: Статус запроса и данные(статус, объект GoodsOnModeration), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods_on_moderation/get_list_by_status/{}'.format(
        status)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def change_moderation_goods_status(moder_id, name, image, new_status):
    """
    Запрос на изменение статуса товара на модерации. Используется в панели администратора

    :param moder_id: Id модератора, запрашивающего изменение статуса
    :param name: Название товара, чей статус должен измениться
    :param image: Файл картинки этого товара
    :param new_status: Статус, который нужно применить
    :return: Статус запроса и данные(статус, объект GoodsOnModeration), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods_on_moderation/detail/{}/'.format(moder_id)
    payload = {'status': new_status, 'name': name, 'image': image}
    response = requests.request("PUT", url, data=payload, headers=API_HEADERS)
    return response.status_code, response.json()


def create_good_with_old_image(name, barcode, category, points, file):
    """
    Создание товара с уже существующей фотографией. Используется в панели администратора

    :param name: Название товара
    :param barcode: Штрих-код товара
    :param category: Категория, к которой отнесли товар
    :param points: Оценка товара командой Продовед
    :param file: Файл с картинкой товара
    :return: Статус запроса и данные(статус, объект Goods), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods/accept/'
    payload = {'name': name, 'barcode': barcode, 'category': category, 'points_rusControl': points,
               'file': file}
    response = requests.request("POST", url, data=payload, headers=API_HEADERS)
    return response.status_code, response.json()


def create_good_with_new_image(name, barcode, category, points, file):
    """
    Создание товара с новой картинкой. Используется в панели администраторов

    :param name: Название товара
    :param barcode: Штрих-код товара
    :param category: Категория, к которой отнесли товар
    :param points: Оценка товара командой Продовед
    :param file: Файл картинки товара
    :return: Статус запроса и данные(статус, объект Goods), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods/create/'
    payload = {'name': name, 'barcode': barcode, 'category': category, 'points_rusControl': points}
    response = requests.request("POST", url, data=payload, headers=API_HEADERS,
                                files={'file': file})
    return response.status_code, response.json()


def get_all_goods_names():
    """
    Получение названий всех товаров с API. Используется для поиска на главной странице

    :return: Статус запроса и данные(статус, список названий всех товаров), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/goods/all_names/'
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_all_categories():
    """
    Получение названий всех категорий с API. Используется для поиска на главной странице

    :return: Статус запроса и данные(статус, список названий всех категорий), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/category/all_names_urls/'
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_amount_of_pictures():
    """
    Получение количества картинок на Api. Используется для статистики на главной странице

    :return: Статус запроса и данные(статус, общее число всех картинок на API), переданные с \
    запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/picture/get_amount/'
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_admin_auth_token(username, password):
    """
    Получение токена для разделения модераторов и администраторов. Используется на странице \
    авторизации администраторов

    :param username: Имя администратора
    :param password: Пароль администратора
    :return: Статус запроса и данные(статус, токен администратора), переданные с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/auth_token/token/login'
    payload = {'username': username, 'password': password}
    response = requests.request("POST", url, data=payload)
    return response.status_code, response.json()


def add_picture_for_product(image, author, good_name):
    """
    Получение продукта по картинке с сервера API. Используется при загрузке фото пользователем \
    для поиска товара по картинке

    :param image: Файл с картинкой для поиска в базе данных
    :param author: Автор запроса(пользователь, загрузивший фото)
    :return: Статус запроса и данные(статус, название товара и способ распознования), переданные \
    с запросом
    """
    url = 'http://api.scanner.savink.in/api/v1/picture/add-to-product/'
    payload = {'platform': 'WEB', 'author': author, 'good': good_name}
    response = requests.request("POST", url, headers=API_HEADERS, data=payload,
                                files={'image': image})
    return response.status_code, response.json()
