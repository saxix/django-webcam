=============
django-webcam
=============

django fields and templetags to store easier webcam snaphot in ImageField ( ie Facebook Profile )

.. note:: It use the jquery.webcam plugin from Robert Eisele (robert@xarg.org)


Examples
--------

models.py::

    class Person(models.Model):
        picture = CameraField(upload_to='photos', blank=True)


urls.py::

    sec('/picture/(?P<pk>\d+)/$'),
        CameraView.as_view(target='registration.Person.picture'), name='picture-mgm')

your template::

    {% load webcam %}

    {% url "picture-mgm" object.pk as picmgm %}
    {% url "camera" object.picture as default_image %}
    {% camera  picmgm default_image %}


Links
~~~~~

   * Project home page: https://github.com/saxix/django-webcam
   * Issue tracker: https://github.com/saxix/django-webcam/issues?sort
   * Download: http://pypi.python.org/pypi/django-webcam/
