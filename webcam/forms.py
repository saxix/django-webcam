from django import forms
from webcam.widgets import CameraWidget


class CameraField(forms.CharField):
    widget = CameraWidget

    def __init__(self, width=320, height=240, camera_width=640, camera_height=280, *args, **kwargs):
        self.width = width
        self.height = height
        self.camera_width = camera_width
        self.camera_height = camera_height
        super(CameraField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {'width': self.width,
                'height': self.height,
                'camera_width': self.camera_width,
                'camera_height': self.camera_height}
