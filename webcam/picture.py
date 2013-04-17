import StringIO
import base64
import logging
from PIL import Image
from django.db.models.fields.files import FieldFile

logger = logging.getLogger(__name__)

class ImageProxyMixin(object):
    image = 1

    def _get_dimension(self):
        return self.image.size

    dimension = property(_get_dimension)
    def _get_image(self):
        try:
            return Image.open(self.get_content())
        except (IOError, ValueError):
            return None
    image = property(_get_image)

    @property
    def width(self):
        return self.dimension[0]

    @property
    def height(self):
        return self.dimension[1]

    def validate(self):
        return self.image is not None

class CameraPicture2(FieldFile, ImageProxyMixin):

    def __init__(self, instance, field, name, stream=None):
        super(FieldFile, self).__init__(None, name)
        self.instance = instance
        self.field = field
        self.storage = field.storage
        self._committed = True
        self.stream = stream

    def load_stream(self, stream):
        self.stream = stream

    def get_content(self):
        buf = base64.decodestring(self.stream)
        return StringIO.StringIO(buf)
        # try:
        #     buf = base64.decodestring(self.stream)
        #     return StringIO.StringIO(buf)
        # except (TypeError, binascii.Error):
        #     return None


    # def _get_image(self):
    #     try:
    #         return Image.open(self.content)
    #     except (IOError, ValueError, AttributeError):
    #         return None
    # image = property(_get_image)


CameraPicture = CameraPicture2
# class CameraPicture(FileProxyMixin, ImageProxyMixin):
#     def __init__(self, stream=None, filename=None, field=None):
#         self.stream = stream
#         self.filename = filename
#         self.field = field
#         self._committed = False
#
#     def __str__(self):
#         return '<CameraPicture>'
#
#     def __repr__(self):
#         return '<CameraPicture>'
#
#     def __unicode__(self):
#         return u'<CameraPicture>'
#
#     def __nonzero__(self):
#         return bool(self.stream)
#
#     def __len__(self):
#         return self.size
#
#     def _require_stream(self):
#         if not self:
#             raise ValueError("The '%s' attribute has no stream associated with it." % self.field.name)
#
#     def _get_file(self):
#         try:
#             buf = base64.decodestring(self.stream)
#             return StringIO.StringIO(buf)
#         except (TypeError, binascii.Error):
#             return None
#
#     file = property(_get_file)
#
#     def _load_bitmap(self, bitmap):
#         self.stream = base64.encodestring(bitmap)
#
#     def _get_image(self):
#         try:
#             return Image.open(self.file)
#         except (IOError, ValueError, AttributeError):
#             return None
#     image = property(_get_image)
#
#
#     def _get_size(self):
#         if self.file:
#             return len(self.file.getvalue())
#         else:
#             raise ValueError()
#     size = property(_get_size)
#
#
#     def _get_name(self):
#         if self.filename:
#             return self.filename
#         return ''
#     name = property(_get_name)
#
#
#     def save(self, name, content):
#         """
#
#         @param name: filename
#         @param content: ContentFile
#         @return:
#         """
#         name = self.field.generate_filename(self.instance, name)
#         if self.field:
#             self.filename = self.field.storage._save(name, content)
# #
