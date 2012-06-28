# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Widget
from django.template.loader import render_to_string, find_template


class CameraWidget(Widget):
    class Media:
        css = {
            'all': ('pretty.css',)
        }
        js = ('webcam/jquery.js',
              'webcam/jquery.webcam.js',
              'webcam/jquery.Jcrop.min.js',
              'webcam/camera.js')


    def render(self, name, value, attrs=None):
        return render_to_string('webcam/camera2.html', {'name':name, 'value':value, 'attrs':attrs})

class CameraField(forms.ImageField):
#    widget = CameraWidget

    def __init__(self, *args, **kwargs):
        super(CameraField, self).__init__(*args, **kwargs)

