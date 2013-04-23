import django.contrib.admin
import django.contrib.admin.sites
from django.contrib.admin import site, ModelAdmin


class PublicAdminSite(django.contrib.admin.sites.AdminSite):
    def has_permission(self, request):
        request.user = User.objects.get_or_create(username='sax')[0]
        return True

site = PublicAdminSite()
django.contrib.admin.site = django.contrib.admin.sites.site = site

from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from demoproject.models import DemoModel
import webcam.admin

class DemoModelAdmin(ModelAdmin):
    list_display = ['photo', 'fullpath']

    def fullpath(self, record):
        return record.storage.path(record.photo)

site.register(DemoModel, DemoModelAdmin)

urlpatterns = patterns('',
    (r'', include(include(site.urls))),
    # url(r'^admin/', include(site.urls)),
)
