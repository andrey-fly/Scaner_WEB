import requests

from Scanner.settings import API_HEADERS


def get_product(image, author):
    url = 'http://api.scanner.savink.in/api/v1/goods/get_product/'
    params = {'platform': 'WEB', 'author': author}
    response = requests.request("GET", url, headers=API_HEADERS, params=params, files={'file': image})
    return response.status_code, response.json()


def get_picture_by_hash(own_hash):
    url = 'http://api.scanner.savink.in/api/v1/picture/get_picture_by_hash/{}'.format(own_hash)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def download_by_hash(own_hash):
    url = 'http://api.scanner.savink.in/api/v1/picture/download_picture_by_hash/{}'.format(own_hash)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response


def create_moderation_good_with_hash(own_hash, name, barcode):
    url = 'http://api.scanner.savink.in/api/v1/goods_on_moderation/create_by_hash/'
    payload = {}
    payload['name'] = name
    payload['barcode'] = barcode
    payload['hash'] = own_hash
    response = requests.request("POST", url, data=payload, headers=API_HEADERS)
    return response.status_code, response.json()


def get_barcode(image):
    url = 'http://api.scanner.savink.in/api/v1/getbarcode/'
    response = requests.request("GET", url, headers=API_HEADERS, files={'file': image}).json()
    barcode = None
    if response['status'] == 'ok':
        barcode = response['barcode']
    return barcode


def get_good_by_name(good):
    url = 'http://api.scanner.savink.in/api/v1/goods/get_by_name/{}/'.format(good)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()


def get_picture_list_by_good_name(good_name):
    url = 'http://api.scanner.savink.in/api/v1/picture/get_pictures_list_by_good_name/{}'.format(good_name)
    response = requests.request("GET", url, headers=API_HEADERS)
    return response.status_code, response.json()
