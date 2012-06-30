from django.db.models.fields.files import ImageField
from webcam import forms


class CameraField(ImageField):
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        super(CameraField, self).__init__(verbose_name, name, width_field, height_field, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CameraField}
        defaults.update(kwargs)
        return super(CameraField, self).formfield(**defaults)

try:
    import south
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^webcam\.models\.CameraField"])
except ImportError:
    pass
