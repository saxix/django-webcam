from django.conf.urls import url, patterns, include
import webcam

urlpatterns = patterns('',
    url(r'^webcam/save$', webcam.views.CameraView.as_view(), name="picture-save", kwargs={'op':'save'}),
    url(r'^webcam/delete$', webcam.views.CameraView.as_view(), name="picture-delete", kwargs={'op':'delete'}),

)
