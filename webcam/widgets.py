from django.forms.widgets import Widget
from django.template.loader import render_to_string


class CameraWidget(Widget):
    template = 'webcam/fswidget.html'

    class Media:
        css = {'all': ('webcam/django-webcam.min.css',)}
        js = ('webcam/jquery-1.7.2.min.js',
              'webcam/jquery.django-webcam.min.js',
              'webcam/django-webcam.js',)

    def render(self, name, value, attrs=None):
        defaults = {'name': name,
                    'format': self.attrs['format'],
                    'width': self.attrs['width'],
                    'height': self.attrs['height'],
                    'camera_width': self.attrs['camera_width'],
                    'camera_height': self.attrs['camera_height'],
                    'picture': value,
                    'attrs': attrs}
        defaults.update(attrs)
        return render_to_string(self.template, defaults)

    def value_from_datadict(self, data, files, name):
        raw_val = data.get("data_%s" % name, None)
        filename = data.get("%s" % name, None)
        if raw_val:
            raw_val = raw_val.replace('data:image/jpeg;base64,', '')
        return (filename, raw_val)
