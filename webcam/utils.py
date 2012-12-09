import StringIO
from base64 import decodestring
import base64
import binascii
from PIL import Image
from django.core.files import File
from django.db.models.fields.files import ImageFieldFile, FieldFile
import os


class InvalidImageFormat(Exception):
    pass


class Base64Image(object):
    def __init__(self, stream, format=None, name=None):
        self._base64 = stream
        self.name = name
        self.format = format

    def __len__(self):
        return len(self._base64)

    def __nonzero__(self):
        return bool(self._base64)

    def __str__(self):
        return self._base64

    def __unicode__(self):
        return self._base64

#        def get_mime(self, format):
#            return 'data:image/%s;base64' % format

    def as_base64(self):
        return self._base64

    def _get_size(self):
        return len(self.as_bitmap())

    size = property(_get_size)

    def as_bitmap(self):
        if not hasattr(self, '_bitmap'):
            try:
                content = self._base64
                self._bitmap = decodestring(content)
            except (binascii.Error, TypeError, AttributeError, ValueError) as e:
                raise InvalidImageFormat(e)
        return self._bitmap

    @property
    def image(self):
        if not hasattr(self, '_image'):
            try:
                self._image = Image.open(StringIO.StringIO(self.as_bitmap()))
            except IOError:
                raise InvalidImageFormat(self._base64)
        return self._image

    def _get_width(self):
        return self._get_image_dimensions()[0]

    width = property(_get_width)

    def _get_height(self):
        return self._get_image_dimensions()[1]

    height = property(_get_height)

    def _get_image_dimensions(self):
        if not hasattr(self, '_dimensions_cache'):
            if self.image:
                self._dimensions_cache = self._image.size
            else:
                self._dimensions_cache = (None, None)
        return self._dimensions_cache


#class Base64ImageFieldFile(Base64Image, File):
#    def __init__(self, instance, field, data, name):
#        File.__init__(self, None, name)
#        self.instance = instance
#        self.field = field
#        self.storage = field.storage
#        self._committed = True
#        self._base64= data
#        self._file = None
#        self.name = None
#
#    def __str__(self):
#        return str(self.name)
#
#    def __unicode__(self):
#        return unicode(self.name)
#
#    def __nonzero__(self):
#        return bool(self._base64)
#
#    def as_base64(self):
#        if not self._base64:
#            try:
#                self._base64 = '%s,%s' % (self.get_mime(), base64.encodestring(self.file.read()))
#            except IOError:
#                return None
#        return self._base64
#
#    def delete(self, save=True):
#        # Clear the image dimensions cache
#        if hasattr(self, '_dimensions_cache'):
#            del self._dimensions_cache
#        super(Base64ImageFieldFile, self).delete(save)
#
#    def save(self):
#        self.storage.save(self)
#
#    def _get_file(self):
#        self._require_file()
#        if not hasattr(self, '_file') or self._file is None:
#            self._file = self.storage.open(self.name, 'rb')
#        return self._file
#
#    def _set_file(self, file):
#        self._file = file
#        if file:
#            self.name = file.name
#
#    def _del_file(self):
#        del self._file
#
#    file = property(_get_file, _set_file, _del_file)
#
#    def _require_file(self):
#        if not self._file:
#            raise ValueError("The '%s' attribute has no file associated with it." % self.field.name)
#
#    @property
#    def filename(self):
#        self._require_file()
#        return os.path.basename(self._file.name)
