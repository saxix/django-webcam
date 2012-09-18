=============
django-webcam
=============

django fields easy store webcam snaphot ( ie Facebook Profile )

.. note:: It use the jquery.webcam plugin from Robert Eisele (robert@xarg.org)



Examples
--------

models.py::

    from webcam.fields import DBCameraField

    class Person(models.Model):
        picture = DBCameraField()


Links
~~~~~

   * Project home page: https://github.com/saxix/django-webcam
   * Issue tracker: https://github.com/saxix/django-webcam/issues?sort
   * Download: http://pypi.python.org/pypi/django-webcam/
