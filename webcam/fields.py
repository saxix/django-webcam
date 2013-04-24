import os
from django.db import models
from django.utils.text import capfirst
from webcam import forms
from webcam.picture import CameraPicture
from webcam.storage import CameraStorage, get_picture_name


class CameraField(models.FileField):
    attr_class = CameraPicture

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', 'jpg')
        super(CameraField, self).__init__(*args, **kwargs)
        self.storage = kwargs.get('storage', CameraStorage())

    def get_filename(self, filename):
        if not filename:
            filename = get_picture_name(self.format)
        return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField,
                    'format': self.format,
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        defaults.update(kwargs)
        return super(CameraField, self).formfield(**defaults)
