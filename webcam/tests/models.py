# -*- coding: utf-8 -*-
from django.db import models
from webcam.fields import CameraPictureField
import random
import tempfile

from django.core.files.storage import FileSystemStorage

temp_storage_location = tempfile.mkdtemp()
temp_storage = FileSystemStorage(location=temp_storage_location)


class FSDemoModel(models.Model):
    def custom_upload_to(self, filename):
        return 'foo'

    def random_upload_to(self, filename):
        # This returns a different result each time,
        # to make sure it only gets called once.
        return '%s/%s' % (random.randint(100, 999), filename)

    # normal = models.FileField(storage=temp_storage, upload_to='tests')
    # custom = models.FileField(storage=temp_storage, upload_to=custom_upload_to)
    # random = models.FileField(storage=temp_storage, upload_to=random_upload_to)
    # default = models.FileField(storage=temp_storage, upload_to='tests', default='tests/default.txt')

    photo = CameraPictureField('FilePictureField', format='jpeg',
                               null=True, blank=True,
                               storage=temp_storage, upload_to='tests')

    class Meta:
        app_label = 'webcam'
