# -*- coding: utf-8 -*-
import tempfile
from django.db import models
from webcam.fields import DBCameraField, FSCameraField
from webcam.storage import CameraFileSystemStorage


class DBDemoModel(models.Model):
    photo = DBCameraField('DatabasePictureField',format='png', null=True, blank=True)

class FSDemoModel(models.Model):
    photo = FSCameraField('FilePictureField',format='jpeg', null=True, blank=True, storage=CameraFileSystemStorage(tempfile.gettempdir()))
