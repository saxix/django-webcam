import tempfile
from django.core.files.storage import FileSystemStorage
from .util import mktree

temp_storage_location = tempfile.mkdtemp(prefix='_webcam')
mktree(temp_storage_location)
temp_storage = FileSystemStorage(location=temp_storage_location)

from .widgets import *  # NOQA
from .camerapicture import *  # NOQA
from .fields import *  # NOQA
