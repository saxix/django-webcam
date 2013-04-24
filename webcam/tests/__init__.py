import tempfile

from .util import mktree
from webcam.storage import CameraStorage

temp_storage_location = tempfile.mkdtemp(prefix='_webcam')
mktree(temp_storage_location)
temp_storage = CameraStorage(location=temp_storage_location)

from .widgets import *  # NOQA
from .fields import *  # NOQA
