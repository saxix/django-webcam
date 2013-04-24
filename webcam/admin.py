# -*- coding: utf-8 -*-
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from webcam import widgets
from webcam.fields import CameraField


FORMFIELD_FOR_DBFIELD_DEFAULTS[CameraField] = {'widget': widgets.FSCameraWidget}
