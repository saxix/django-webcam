from django.db import models
from webcam.fields import DBCameraField, FSCameraField


class DemoModel(models.Model):
    photo1 = DBCameraField('DatabasePictureField', null=True, blank=True)
    photo2 = FSCameraField('FilePictureField', null=True, blank=True)
