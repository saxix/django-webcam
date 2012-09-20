from django.db import models
from webcam.fields import DBCameraField, FSCameraField


class DemoModel(models.Model):
    photo1 = DBCameraField('DatabasePictureField',format='png', null=True, blank=True)
    photo2 = FSCameraField('FilePictureField',format='jpeg', null=True, blank=True)
