.. _install:

.. include:: globals.rst

Installation
============

Installing |app| is as simple as checking out the source and adding it to
your project or ``PYTHONPATH``.


1. Either check out django-adminactions from `GitHub`_ or to pull a release off `PyPI`_. Doing ``pip install django-webcam`` or ``easy_install django-webcam`` is all that should be required.

2. Either symlink the ``webcam`` directory into your project or copy the directory in. What ever works best for you.


Configuration
=============

Add :mod:`webcam` to your :setting:`INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'webcam',
        ...
    )
