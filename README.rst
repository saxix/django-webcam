===================
django-webcam
===================

django fields to get and store webcam snaphot

* fully compatible with Django FileField protocol
* Supports gif/jpeg/png
* Manage multiple fields in the same page
* Works in the admin as any other field ( need ``import webcam.admin`` to configure ``FORMFIELD_FOR_DBFIELD_DEFAULTS``)

.. note:: based on jquery.webcam plugin from Robert Eisele (robert@xarg.org)


Examples
========


models.py::

    import webcam.admin # needed to show the right widget in the admin
    from django.db import models
    from webcam.fields import CameraField

    class Person(models.Model):
        picture = CameraField()

Links
=====

   * Project home page: https://github.com/saxix/django-webcam
   * Issue tracker: https://github.com/saxix/django-webcam/issues?sort
   * Download: http://pypi.python.org/pypi/django-webcam/
