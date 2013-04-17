from django import forms
from webcam.widgets import FSCameraWidget


class CameraField(forms.CharField):
    widget = FSCameraWidget

    def __init__(self, width=320, height=240, format='jpg',
                 camera_width=320, camera_height=240, *args, **kwargs):
        self.format = format
        self.width = width
        self.height = height
        self.camera_width = camera_width
        self.camera_height = camera_height
        kwargs['max_length'] = None
        kwargs['min_length'] = None
        super(CameraField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {'width': self.width,
                'height': self.height,
                'format': self.format,
                'camera_width': self.camera_width,
                'camera_height': self.camera_height}
