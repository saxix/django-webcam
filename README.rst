
===================
django-webcam
===================

django fields easy store webcam snaphot ( ie Facebook Profile )

* Can store in database or filesystem
* Support gif/jpeg/png
* Manage multiple fields in the same page
* Works in the admin as any other field

.. note:: based on jquery.webcam plugin from Robert Eisele (robert@xarg.org)



Examples
========


models.py::

    from django.db import models
    from webcam.fields import DBCameraField, FSCameraField
    from webcam.storage import CameraFileSystemStorage

    class Person(models.Model):
        picture1 = DBCameraField() # store in the database
        picture2 = FSCameraField(format='gif') # by default storen on settings.MEDIA_ROOT
        picture3 = FSCameraField(format='png',
                                 storage=CameraFileSystemStorage('/absolute/path/to/'),
                                 null=True, blank=True) # store on filesystem


Links
=====

   * Project home page: https://github.com/saxix/django-webcam
   * Issue tracker: https://github.com/saxix/django-webcam/issues?sort
   * Download: http://pypi.python.org/pypi/django-webcam/
