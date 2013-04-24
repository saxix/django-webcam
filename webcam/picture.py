import base64
import logging
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class PictureUploadedFile(SimpleUploadedFile):
    def __init__(self, name, content, content_type='text/plain'):
        super(PictureUploadedFile, self).__init__(name, content, content_type)

try:
    from PIL import Image

    class ImageProxyMixin(object):

        @cached_property
        def image(self, bitmap=None):
            c = bitmap or self
            try:
                self._image = Image.open(c)
                return self._image
            except IOError as e:  # cannot identify image file
                raise ValueError(e)

except ImportError:
    class ImageProxyMixin(object):
        @property
        def image(self, bitmap=None):
            raise Exception('Cannot access to `image` property. Please install PIL/pillow')


class CameraPicture(FieldFile, ImageProxyMixin):

    @property
    def stream(self):
        try:
            buf = self.file.read()
            return base64.encodestring(buf)
        except IOError:
            return ''
        except ValueError:
            return ''

    @cached_property
    def dimension(self):
        return self.image.size

    @property
    def width(self):
        return self.dimension[0]

    @property
    def height(self):
        return self.dimension[1]
