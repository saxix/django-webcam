# -*- coding: utf-8 -*-
from django.db import models
from webcam.fields import CameraPictureField
import random

# temp_storage_location = tempfile.mkdtemp()
# temp_storage = FileSystemStorage(location=temp_storage_location)
from webcam.tests import temp_storage


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

    photo = CameraPictureField('CameraPictureField', format='jpeg',
                               null=True, blank=True,
                               storage=temp_storage, upload_to='tests')

    class Meta:
        app_label = 'webcam'
