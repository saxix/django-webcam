# -*- coding: utf-8 -*-
import os
import uuid
from django.core.files.storage import FileSystemStorage


def get_picture_name(suffix='jpg'):
    return "{0}.{1}".format(uuid.uuid4(), suffix)


class CameraStorage(FileSystemStorage):

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(self.path(name))
        return name
