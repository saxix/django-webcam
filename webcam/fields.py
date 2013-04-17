from django.db import models
from django.db.models.fields.files import FileDescriptor
from django.utils.text import capfirst
from webcam import forms
from webcam.picture import CameraPicture2

class StreamContent(object):
    def __init__(self, stream):
        self.stream = stream
    def __str__(self):
        return self.stream
    def __repr__(self):
        return self.stream


class CameraPictureDescriptor(FileDescriptor):
    # def __init__(self, field):
    #     self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        file = instance.__dict__[self.field.name]
        if file is None:
            picture = self.field.attr_class(instance, self.field, '', str(file))
            picture._committed = False
            instance.__dict__[self.field.name] = picture
            return instance.__dict__[self.field.name]

        if isinstance(file, StreamContent):
            picture = self.field.attr_class(instance, self.field, '', str(file))
            picture._committed = False
            instance.__dict__[self.field.name] = picture
            return instance.__dict__[self.field.name]

        return super(CameraPictureDescriptor, self).__get__(instance, owner)
        # picture = instance.__dict__[self.field.name]
        # if isinstance(file, CameraPicture):
        #     picture.instance = instance
        #     picture.field = self.field
        #     picture.storage = self.field.storage
        #
        #  # That was fun, wasn't it?
        # return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class CameraPictureField(models.FileField):
    # __metaclass__ = models.SubfieldBase
    descriptor_class = CameraPictureDescriptor
    attr_class = CameraPicture2

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', 'jpg')
        super(CameraPictureField, self).__init__(*args, **kwargs)

    # def to_python(self, value):
    #     print 1111111, value
        # if isinstance(value, CameraPicture):
        #     return value
        # return CameraPicture(stream=value, field=self)

    # def save_form_data(self, instance, data):
    #     super(CameraPictureField, self).save_form_data(instance, data)

    # def get_prep_value(self, value):
    #     if isinstance(value, CameraPicture) and value:
    #         return value.name
    #     return CameraPicture()

    # def contribute_to_class(self, cls, name):
    #     self.set_attributes_from_name(name)
    #     self.model = cls
    #     cls._meta.add_field(self)
    #     if self.choices:
    #         setattr(cls, 'get_%s_display' % self.name,
    #                 curry(cls._get_FIELD_display, field=self))

    def save_form_data(self, instance, data):
        # field = getattr(instance, self.name)
        # field.load_stream(data)
        data = StreamContent(data)
        super(CameraPictureField, self).save_form_data(instance, data)

    # def pre_save(self, model_instance, add):
    #     getattr(model_instance, self.attname)
    #     picture = super(CameraPictureField, self).pre_save(model_instance, add)
    #     if picture and not picture._committed:
    #         picture.save(picture.name, picture, save=False)
    #     return picture

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField,
                    'format': self.format,
                    # 'width': self.widget_width,
                    # 'height': self.widget_height,
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        defaults.update(kwargs)
        return super(CameraPictureField, self).formfield(**defaults)

    # def clean(self, value, model_instance):
    #     value = super(CameraPictureField, self).clean(value, model_instance)
    #     if not value.validate():
    #         raise ValidationError('Not valid image')
    #     return value
