from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.widgets import Widget
from django.template.loader import render_to_string


class CameraWidget(Widget):
    class Media:
        css = {
            'all': ('webcam/webcam.css',)
        }
        js = (
            'webcam/jquery-1.7.2.min.js',
            'webcam/jquery.webcam.min.js',
            'webcam/widget.min.js',
            )

    def render(self, name, value, attrs=None):
        defaults = {'name': name,
                    'width': self.attrs['width'],
                    'height': self.attrs['height'],
                    'camera_width': self.attrs['camera_width'],
                    'camera_height': self.attrs['camera_height'],
                    'value': value,
                    'attrs': attrs}
        defaults.update(attrs)
        return render_to_string(self.template, defaults)


class DBCameraWidget(CameraWidget):
    template = 'webcam/dbwidget.html'


class FSCameraWidget(CameraWidget):
    template = 'webcam/fswidget.html'

    def value_from_datadict(self, data, files, name):
        filename = data.get(name, None)
        image = data.get("data_%s" % name, None)
        return "%s|%s" % (filename, image)

    def render(self, name, value, attrs=None):
        filename, data = value.split('|')
        attrs = attrs or {}
        attrs.update({'value': filename, 'image': data, })
        return super(FSCameraWidget, self).render(name, value, attrs)

