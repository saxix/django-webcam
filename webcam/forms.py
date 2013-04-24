import base64
import uuid
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from webcam.picture import CameraPicture
from webcam.widgets import FSCameraWidget

class NoName(object):
    def __str__(self):
        return ''



class CameraField(forms.FileField):
    widget = FSCameraWidget

    def __init__(self, width=320, height=240, format='jpg',
                 camera_width=320, camera_height=240, *args, **kwargs):
        self.format = format
        self.width = width
        self.height = height
        self.camera_width = camera_width
        self.camera_height = camera_height
        # kwargs['max_length'] = None
        # kwargs['min_length'] = None
        super(CameraField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {'width': self.width,
                'height': self.height,
                'format': self.format,
                'camera_width': self.camera_width,
                'camera_height': self.camera_height}

    def to_python(self, data):
        filename, raw_val = data
        if raw_val:
            return SimpleUploadedFile(filename, base64.decodestring(raw_val))

    def clean(self, data, initial=None):
        filename, raw_val = data
        # maybe the form do not use the right CameraWidget ?
        if not filename:
            if initial:
                filename = initial.name
            else:
                filename = "{0}.{1}".format(uuid.uuid4(), self.format)

        return super(CameraField, self).clean((filename, raw_val), initial)

