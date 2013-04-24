import base64
import logging
from PIL import Image
from django.core.files.base import ContentFile, File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.utils.encoding import smart_str, smart_unicode
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)

STREAM = -999

NO_CHANGES = object()

# class StreamContent(object):
#     def __init__(self, stream):
#         self._stream = stream
#
#     def __str__(self):
#         return self._stream or ''
#
#     def __repr__(self):
#         return '<StreamContent>'
#
#     @property
#     def stream(self):
#         if self._stream:
#             return str(self._stream)
#         return None
#
# class SameContent(object):
#     def __init__(self, picture):
#         self.picture = picture

class PictureUploadedFile(SimpleUploadedFile):
    def __init__(self, name, content, content_type='text/plain'):
        super(PictureUploadedFile, self).__init__(name, content, content_type)


class CameraPicture(FieldFile):

    # def __str__(self):
    #     return smart_str(self.name or '')
    #
    # def __unicode__(self):
    #     return smart_unicode(self.name or u'')
    #
    # def __repr__(self):
    #     return "<%s: '%s'>" % (self.__class__.__name__, self or "None")
    #
    # @property
    # def stream(self):
    #     try:
    #         buf = self.file.read()
    #         return base64.encodestring(buf)
    #     except IOError:
    #         return ''
    #     except ValueError:
    #         return ''

    # def __nonzero__(self):
    #     return bool(self.name) or bool(self._file)

    # def get_base64(self):
    #     return base64.decodestring(self.stream)

    def _get_dimension(self):
        return self.image.size

    dimension = property(_get_dimension)

    @property
    def image(self, bitmap=None):
        if getattr(self, '_image', None):
            return self._image

        c = bitmap or self
        try:
            self._image = Image.open(c)
            return self._image
        except IOError as e:  # cannot identify image file
            raise ValueError(e)

    @property
    def width(self):
        return self.dimension[0]

    @property
    def height(self):
        return self.dimension[1]

    # def save(self, name, content, save=True):
    #     name = self.field.generate_filename(self.instance, name)
    #     if content == STREAM:
    #         content = ContentFile(self.read())
    #
    #     name = self.storage.save(name, content)
    #     setattr(self.instance, self.field.name, name)
    #     # Update the filesize cache
    #     self.name = name
    #     self.file = File(self.storage.open(self.name), self.name)
    #     self._size = self.file.size
    #     self._committed = True
    #     self._image = None
    #
    #     # Save the object because it has changed, unless save is False
    #     if save:
    #         self.instance.save()
    #
    # save.alters_data = True

