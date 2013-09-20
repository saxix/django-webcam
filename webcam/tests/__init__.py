from __future__ import absolute_import
import tempfile

from .util import mktree
from webcam.storage import CameraStorage

temp_storage_location = tempfile.mkdtemp(prefix='_webcam')
mktree(temp_storage_location)
temp_storage = CameraStorage(location=temp_storage_location)

from .test_widgets import *  # NOQA
from .test_fields import *  # NOQA
