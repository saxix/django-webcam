
===================
django-webcam
===================

django fields easy store webcam snaphot ( ie Facebook Profile )

* Can store in database or filesystem
* Support gif/jpeg/png
* Manage multiple image fields in the same page


.. note:: based on jquery.webcam plugin from Robert Eisele (robert@xarg.org)



Examples
========


models.py::

    from webcam.fields import DBCameraField
    from webcam.fields import FileSystemStorage


    class Person(models.Model):
        picture1 = DBCameraField() # store in the database
        picture2 = FSCameraField(format='gif') # by default storen on settings.MEDIA_ROOT
        picture3 = FSCameraField(format='png',
                                 storage=FileSystemStorage('/absolute/path/to/'),
                                 null=True, blank=True) # store on filesystem


Links
=====

   * Project home page: https://github.com/saxix/django-webcam
   * Issue tracker: https://github.com/saxix/django-webcam/issues?sort
   * Download: http://pypi.python.org/pypi/django-webcam/
   * Documentation: http://django-webcam.readthedocs.org/en/latest/
