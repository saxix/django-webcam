# -*- coding: utf-8 -*-
from django.db import models
from webcam.fields import CameraField
from webcam.tests import temp_storage


class WebcamTestModel(models.Model):
    photo = CameraField('CameraPictureField', format='jpeg', null=True, blank=True,
                               storage=temp_storage, upload_to='tests')

    class Meta:
        app_label = 'webcam'
