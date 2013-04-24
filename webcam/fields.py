import base64
import os
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models.fields.files import FileDescriptor, FieldFile
from django.core.files.base import File, ContentFile
from django.utils.text import capfirst
from webcam import forms
from webcam.picture import CameraPicture
from webcam.storage import WebcamStorage


class CameraPictureDescriptor(FileDescriptor):
    # def __get__(self, instance=None, owner=None):
    #     if instance is None:
    #         raise AttributeError(
    #             "The '%s' attribute can only be accessed from %s instances."
    #             % (self.field.name, owner.__name__))
    #
    #     file = instance.__dict__[self.field.name]
    #     print 'get', type(file),
    #     print repr(file)
    #     if file is None:
    #         picture = self.field.attr_class(instance, self.field, '')
    #         picture._committed = False
    #         picture.file = None
    #         instance.__dict__[self.field.name] = picture
    #         # return instance.__dict__[self.field.name]
    #     elif isinstance(file, basestring):
    #         picture = self.field.attr_class(instance, self.field, file)
    #         picture.name = file
    #         picture._loaded = True
    #         instance.__dict__[self.field.name] = picture
    #     elif isinstance(file, SameContent):
    #         instance.__dict__[self.field.name] =file.picture
    #         # return instance.__dict__[self.field.name]
    #     elif isinstance(file, StreamContent):
    #         picture = self.field.attr_class(instance, self.field, '')
    #         picture._committed = False
    #         if file.stream:
    #             buf = base64.decodestring(file.stream)
    #         else:
    #             buf = ''
    #         picture.file = ContentFile(buf)
    #         instance.__dict__[self.field.name] = picture
    #         # return instance.__dict__[self.field.name]
    #     elif isinstance(file, File) and not isinstance(file, FieldFile):
    #         picture = self.field.attr_class(instance, self.field, file.name)
    #         picture.file = file
    #         # if file.name is None:
    #         #     picture.name = "{0}.{1}".format(uuid.uuid4(), self.field.format)
    #         picture._committed = False
    #         instance.__dict__[self.field.name] = picture
    #         return instance.__dict__[self.field.name]
    #     elif isinstance(file, CameraPicture):
    #         pass
    #     elif isinstance(file, FieldFile) and not hasattr(file, 'field'):
    #         file.instance = instance
    #         file.field = self.field
    #         file.storage = self.field.storage
    #     else:
    #         raise Exception(file)
    #     return instance.__dict__[self.field.name]
    #     # return super(CameraPictureDescriptor, self).__get__(instance, owner)
    #
    def __set__(self, instance, value):
        print 'set', instance, type(value)
        instance.__dict__[self.field.name] = value


class CameraPictureField(models.FileField):
    # descriptor_class = CameraPictureDescriptor
    attr_class = CameraPicture

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', 'jpg')
        self.storage = kwargs.get('storage', WebcamStorage)
        super(CameraPictureField, self).__init__(*args, **kwargs)

    def get_filename(self, filename):
        if not filename:
            filename = "{0}.{1}".format(uuid.uuid4(), self.format)
        return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))

    # def save_form_data(self, instance, data):
    #     if isinstance(data, CameraPicture): # no data changed
    #         # data = SameContent(data)
    #         # data = SameContent(data)
    #         pass
    #     else:
    #         data = StreamContent(data)
    #         # data = SimpleUploadedFile(None, PICTURE)
    #     super(CameraPictureField, self).save_form_data(instance, data)

    # def clean(self, value, model_instance):
    #     return super(CameraPictureField, self).clean(value, model_instance)

    # def pre_save(self, model_instance, add):
    #     camerapicture = getattr(model_instance, self.attname)
    #     if camerapicture and not camerapicture._committed:
    #         camerapicture.save(camerapicture.name, STREAM, save=False)
    #     return camerapicture

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField,
                    'format': self.format,
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        defaults.update(kwargs)
        return super(CameraPictureField, self).formfield(**defaults)
