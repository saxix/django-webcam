import django.contrib.admin
import django.contrib.admin.sites
from django.contrib.auth.models import User
from django.conf.urls import patterns, include


class PublicAdminSite(django.contrib.admin.sites.AdminSite):
    def has_permission(self, request):
        request.user = User.objects.get_or_create(username='sax')[0]
        return True

site = PublicAdminSite()
django.contrib.admin.site = django.contrib.admin.sites.site = site

urlpatterns = patterns('',
    (r'', include(include(site.urls))),
    # url(r'^admin/', include(site.urls)),
)
