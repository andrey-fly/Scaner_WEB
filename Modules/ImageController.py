import os

from django.core.files.storage import FileSystemStorage
from PIL import Image

from API_App.models import *


class ImageController:
    __fs = FileSystemStorage()

    def __init__(self):
        self.__file = None
        self.file_name = None
        self.__imagePIL = None
        self.size = 0

    def save(self, request_file):
        self.__file = request_file
        self.file_name = self.__fs.get_available_name(self.__file.name)
        self.__fs.save(self.file_name, self.__file)
        self.__imagePIL = Image.open('collectedmedia/{}'.format(self.file_name))
        self.size = os.stat('collectedmedia/{}'.format(self.file_name)).st_size

        # s3_link = models.CharField(verbose_name='Ссылка на s3 хранилище', max_length=255)
        # width = models.IntegerField()
        # height = models.IntegerField()
        # good = models.ForeignKey(to=Goods, on_delete=models.CASCADE)

        return self.file_name

    def send_to_s3(self, target_good, platform):
        p = Picture(file=self.__file,
                    target_good=target_good,
                    platform=platform)
        p.save()

    def crop(self, x, y, width, height):
        self.__imagePIL = self.__imagePIL.crop((x, y, width, height))
        self.__imagePIL.save(self.file_name)
        self.size = os.stat('collectedmedia/{}'.format(self.file_name)).st_size

    def compression(self, quality=100):
        self.__imagePIL.resize(self.__imagePIL.size, Image.ANTIALIAS)
        self.__imagePIL.save('collectedmedia/{}'.format(self.file_name), quality=quality, optimize=True)
        self.size = os.stat('collectedmedia/{}'.format(self.file_name)).st_size
        return self.size

    def delete_image(self):
        try:
            os.remove('collectedmedia/{}'.format(self.file_name), dir_fd=None)
            self.__file = None
            self.file_name = None
            self.__imagePIL = None
            self.size = 0
            return True
        except FileNotFoundError:
            return False

    def get_file_name(self):
        return self.file_name
    
    def get_size(self):
        return self.size