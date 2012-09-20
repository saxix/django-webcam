import errno
import base64
import os
import uuid
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.db.models import Field
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.utils._os import safe_join, abspathu
from webcam import forms, widgets


class FileSystemStorage(object):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.MEDIA_ROOT
        self.base_location = location
        self.location = abspathu(self.base_location)
        if base_url is None:
            base_url = settings.MEDIA_URL
        self.base_url = base_url

    def path(self, name):
        try:
            path = safe_join(self.location, name)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)

    def exists(self, name):
        return os.path.exists(self.path(name))

    def get_valid_name(self, name, format):
        newname = str(uuid.uuid4())
        if format:
            return "%s.%s" % (newname, format)
        return newname

    def get_values(self, data):
        filename =''
        image = None
        if data:
            try:
                filename, image = data.split('|')
            except ValueError:
                filename = self.get_valid_name(filename)
        return filename, image

    def get_mime(self, field):
        return 'data:image/%s;base64' % field.format

    def load(self, field, instance):
        try:
            name = getattr(instance, field.attname)
            full_path = self.path(name)
            with open(full_path, 'r') as fd:
                return '%s,%s' % (self.get_mime(field), base64.encodestring(fd.read()))
        except IOError, e:
            return None

    def save(self, field, instance, data):
        name, image = self.get_values(data)
        if not name:
            name = self.get_valid_name(name, field.format)
        if image:
            full_path = self.path(name)
            directory = os.path.dirname(full_path)
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except OSError, e:
                    if e.errno != errno.EEXIST:
                        raise

            if not os.path.isdir(directory):
                raise IOError("%s exists and is not a directory." % directory)

            encode = self.get_mime(field)
            with open(full_path, "wb") as fd:
                fd.write(base64.decodestring(image[len(encode):]))

            setattr(instance, field.name, name)


class CameraField(Field):
    description = _("Picture")

    def __init__(self, verbose_name=None, name=None, width=320, height=240, format='jpeg', **kwargs):
        for arg in ('primary_key', 'unique'):
            if arg in kwargs:
                raise TypeError("'%s' is not a valid argument for %s." % (arg, self.__class__))
        if format not in ['gif', 'jpeg', 'png']:
            raise TypeError("'%s' is not a valid format. ([gif|jpg|png])" % type)

        self.format = format
        self.width = width
        self.height = height
        super(CameraField, self).__init__(verbose_name, name, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField,
                    'format': self.format,
                    'width': self.width,
                    'height': self.height,
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        defaults.update(kwargs)
        return super(CameraField, self).formfield(**defaults)


class DBCameraField(CameraField):
    """
        Camera field that store the picture into the database
    """

    def formfield(self, **kwargs):
        kwargs['widget'] = widgets.DBCameraWidget
        return super(DBCameraField, self).formfield(**kwargs)


class FSCameraField(CameraField):
    """
        Camera field that store the picture as file just like ImageField
    """

    def __init__(self, verbose_name=None, name=None, width=320, height=240, storage=None, **kwargs):
        self.storage = storage or FileSystemStorage()
        super(FSCameraField, self).__init__(verbose_name, name, width, height, **kwargs)

    def value_from_object(self, obj):
        return "%s|%s" % (getattr(obj, self.attname, ''), self.storage.load(self, obj) or "")

    def save_form_data(self, instance, data):
        self.storage.save(self, instance, data)

    def formfield(self, **kwargs):
        kwargs['widget'] = widgets.FSCameraWidget
        return super(FSCameraField, self).formfield(**kwargs)


try:
    import south
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^webcam\.fields\.DBCameraField"])
    add_introspection_rules([], ["^webcam\.fields\.FSCameraField"])
except ImportError:
    pass
