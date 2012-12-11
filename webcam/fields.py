import StringIO
from base64 import decodestring
import base64
import uuid
import binascii
from django.db.models import Field
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
import os
from webcam import forms, widgets
from webcam.storage import CameraFileSystemStorage
from PIL import Image
from webcam.utils import InvalidImageFormat, Base64Image

class CameraPictureDescriptor(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        data_or_filename = instance.__dict__[self.field.name]

        if isinstance(data_or_filename, basestring) or data_or_filename is None:
            if isinstance(self.field, FSCameraField):
                if data_or_filename:
                    with self.field.storage.open(data_or_filename, 'r') as fd:
                        c = fd.read()
                        value = base64.encodestring(c)
                else:
                    value = None
                attr = self.field.attr_class(value, name=data_or_filename)
            else:
                attr = self.field.attr_class(data_or_filename)
        elif isinstance(data_or_filename, (Base64Image, )):
            attr = data_or_filename

        instance.__dict__[self.field.name] = attr

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value

class DBCameraPictureDescriptor(CameraPictureDescriptor):
    pass

class FSCameraPictureDescriptor(CameraPictureDescriptor):
    pass

class CameraField(Field):
    description = _("Picture")

    descriptor_class = CameraPictureDescriptor

    def __init__(self, verbose_name=None, name=None, format='jpeg', widget_width=320, widget_height=240,
                 width_field=None, height_field=None, **kwargs):
        for arg in ('primary_key', 'unique'):
            if arg in kwargs:
                raise TypeError("'%s' is not a valid argument for %s." % (arg, self.__class__))
        if format not in ['gif', 'jpeg', 'png']:
            raise TypeError("'%s' is not a valid format. ([gif|jpeg|png])" % format)

        self.format = format
        self.widget_width = widget_width
        self.widget_height = widget_height
        self.width_field, self.height_field = width_field, height_field
        super(CameraField, self).__init__(verbose_name, name, **kwargs)


    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField,
                    'format': self.format,
                    'width': self.widget_width,
                    'height': self.widget_height,
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        defaults.update(kwargs)
        return super(CameraField, self).formfield(**defaults)

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        has_dimension_fields = self.width_field or self.height_field
        if not has_dimension_fields:
            return

    def contribute_to_class(self, cls, name):
        super(CameraField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

#    def get_mime(self, format):
#        return 'data:image/%s;base64' % format

class DBCameraField(CameraField):
    """
        Camera field that store the picture into the database
    """
    attr_class = Base64Image

    def pre_save(self, model_instance, add):
        attr = getattr(model_instance, self.attname)
        return attr.as_base64()

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        kwargs['widget'] = widgets.DBCameraWidget
        return super(DBCameraField, self).formfield(**kwargs)


class FSCameraField(CameraField):
    """
        Camera field that store the picture as file just like ImageField
    """
    attr_class = Base64Image

    def __init__(self, verbose_name=None, name=None, format='jpeg', widget_width=320, widget_height=240,
                 width_field=None, height_field=None, storage=None, **kwargs):
        self.storage = storage or CameraFileSystemStorage()
        super(FSCameraField, self).__init__(verbose_name, name, format, widget_width, widget_height,
                                            width_field, height_field, max_length=100, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def value_from_object(self, obj):
        return self.storage.load(self, obj) or ""

    def get_prep_value(self, value):
        """
        Perform preliminary non-db specific value checks and conversions.
        """
        if isinstance(value, self.attr_class):
            return str(value)
        return value

    def bind(self, fieldmapping, original, bound_field_class):
        return bound_field_class(self, fieldmapping, original)

    def pre_save(self, model_instance, add):
        attr = getattr(model_instance, self.attname)
        if attr:
            filename = self.get_filename(model_instance)
            if add:
                attr.file = self.storage.open(filename, 'wb')
                attr.name = filename
            self.storage.save(attr)
            return filename
        return None

    def get_filename(self, instance):
        return str(getattr(instance, self.name).name or "%s.%s" % (str(uuid.uuid4()), self.format))

    def save_form_data(self, instance, data):
        filename = self.get_filename(instance)
        attr = getattr(instance, self.attname)
        setattr(instance, self.name, filename)

    def formfield(self, **kwargs):
        kwargs['widget'] = widgets.FSCameraWidget
        return super(FSCameraField, self).formfield(**kwargs)

    def to_python(self, value):
        """
        Converts the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Returns the converted value. Subclasses should override this.
        """
        return value

    def _get_val_from_obj(self, obj):
        if obj is not None:
            return getattr(obj, self.attname)
        else:
            return self.get_default()

try:
    import south
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^webcam\.fields\.DBCameraField"])
    add_introspection_rules([], ["^webcam\.fields\.FSCameraField"])
except ImportError:
    pass


