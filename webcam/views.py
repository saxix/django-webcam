# Create your views here.
from StringIO import StringIO
import json
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from django.core.files.uploadedfile import InMemoryUploadedFile
import time

class CameraView(View):
    target = None
    target_field_name = None
    target_model = None
    target_dest_dir = None
    target_field_object = None

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        op = request.POST.get('op', None)
        if op == 'save':
            return self._save(request, *args, **kwargs)
        elif op == 'rem':
            return self._delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    @classonlymethod
    def as_view(cls, **initkwargs):
        target = initkwargs.get('target', '')
        bits = target.split('.')
        if len(bits) != 3:
            raise ImproperlyConfigured(
                'CameraView.as_view require a `target` argument in the format `app_label.model.field`')
        app_label, model_name, field_name = bits
        model = get_model(app_label, model_name)
        field_object, _, _, _= model._meta.get_field_by_name(field_name)

        initkwargs['target_model'] = model
        initkwargs['target_field_object'] = field_object
        initkwargs['target_field_name'] = field_name
        initkwargs['target_dest_dir'] = field_object.upload_to


        return super(CameraView, cls).as_view(**initkwargs)

    #ImageFieldFile
    def _delete(self, request, *args, **kwargs):
        try:
            target = self.target_model.objects.get(pk=self.kwargs['pk'])
            old_value = getattr(target, self.target_field_name)
            old_value.delete()
            target.save()
        except (IOError, OSError):
            pass
        return HttpResponse(json.dumps({
            'file': '',
            'url': '',
            'old': '',
            'refresh': "?%s" % time.time()
        }))


    def _save(self, request, *args, **kwargs):
        if self.request.POST['type'] == "pixel":
            pass
        elif self.request.POST['type'] == u"data":
            target = self.target_model.objects.get(pk=self.kwargs['pk'])
            raw_data = self.request.POST['image'][len('data:image/png;base64,'):].decode('base64')
            buf = StringIO(raw_data)
            buf.seek(0, 2)
            filename = "%s.png" % target.pk
            file = InMemoryUploadedFile(buf, "picture", filename, None, buf.tell(), None)
            old_picture = getattr(target, self.target_field_name)
            try:
                old_picture.delete()
            except OSError:
                pass
            setattr(target, 'picture', file)
            target.save()
            new_picture = getattr(target, self.target_field_name)
            full_url = reverse('camera', args=[new_picture.url])
        return HttpResponse(json.dumps({
            'file': filename,
            'url': full_url,
            'old': str(old_picture),
            'refresh': "%s?%s" % (full_url, time.time())
        }))
