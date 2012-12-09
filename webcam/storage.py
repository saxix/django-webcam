import errno
import os
import base64
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils._os import safe_join, abspathu


class CameraFileSystemStorage(object):
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

    def file(self, name):
        return file(self.path(name))

    def exists(self, name):
        return os.path.exists(self.path(name))

    def open(self, filename, mode='rb'):
        full_path = self.path(filename)
        return open(full_path, mode)

    def load(self, field, instance):
        try:
            filename = getattr(instance, field.attname)
            with self.open(filename, 'r') as fd:
                return '%s,%s' % (filename.get_mime(), base64.encodestring(fd.read()))
        except IOError:
            return None

    def save(self, attr):
        if attr:
            full_path = self.path(attr.file.name)
            directory = os.path.dirname(full_path)
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except OSError, e:
                    if e.errno != errno.EEXIST:
                        raise

            if not os.path.isdir(directory):
                raise IOError("%s exists and is not a directory." % directory)

            with open(full_path, "wb") as fd:
                fd.write( attr.as_bitmap() )
