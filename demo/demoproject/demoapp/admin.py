from django.contrib.admin import site, ModelAdmin
from demoproject.demoapp.models import DemoModel

class DemoAdmin(ModelAdmin):
    list_display = ('photo2', )

    def format(self):
        return ''

    def format(self):
        return ''

site.register(DemoModel, DemoAdmin)
