# Create your views here.
import os
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import View

class CameraView(View):

    def post(self, request, *args, **kwargs):
        if 'save' in self.kwargs.values():
            return self._save(request, *args, **kwargs)
        elif 'delete' in self.kwargs.values():
            return self._delete(request, *args, **kwargs)

    def _getfilename(self):
        u = self.request.user
        return os.path.join(settings.MEDIA_ROOT, 'profiles', "%s.png" % u.pk )

    def _delete(self, request, *args, **kwargs):
        try:
            os.unlink(self._getfilename() )
        except (IOError, OSError):
            pass
        return HttpResponse('ok')

    def _save(self, request, *args, **kwargs):
        if self.request.POST['type'] == "pixel":
            pass
        elif self.request.POST['type'] == u"data":
            image_data = self.request.POST['image']
            with open( self._getfilename() , "wb" ) as f:
                f.write(image_data[len('data:image/png;base64,'):].decode('base64'))

        return HttpResponse('ok')
