.. include:: globals.rst
.. _index:

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

    class Person(models.Model):
        picture1 = DBCameraField() # store in the database
        picture2 = FSCameraField() # store on filesystem


Links
=====

   * Project home page: https://github.com/saxix/django-webcam
   * Issue tracker: https://github.com/saxix/django-webcam/issues?sort
   * Download: http://pypi.python.org/pypi/django-webcam/
