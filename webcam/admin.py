# -*- coding: utf-8 -*-
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from webcam import widgets
from webcam.fields import CameraPictureField


FORMFIELD_FOR_DBFIELD_DEFAULTS[CameraPictureField] = {'widget': widgets.FSCameraWidget}
