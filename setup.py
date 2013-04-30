#!/usr/bin/env python
from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES
import os
import webcam as app


NAME = app.NAME
RELEASE = app.get_version()

VERSIONMAP = {'final': (app.VERSION, 'Development Status :: 5 - Production/Stable'),
              'rc': (app.VERSION, 'Development Status :: 4 - Beta'),
              'beta': (app.VERSION, 'Development Status :: 4 - Beta'),
              'alpha': ('master', 'Development Status :: 3 - Alpha')}
download_tag, development_status = VERSIONMAP[app.VERSION[3]]


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


def scan_dir(target, packages=[], data_files=[]):
    for dirpath, dirnames, filenames in os.walk(target):
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'):
                del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return packages, data_files

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


packages, data_files = scan_dir('webcam')

setup(
    name=NAME,
    version=RELEASE,
    url='https://github.com/saxix/django-webcam',
    download_url='https://github.com/saxix/django-webcam/tarball/master',
    author='sax',
    author_email='sax@os4d.org',
    description="django fields easy store webcam snaphot",
    license='BSD',
    packages=packages,
    data_files=data_files,
    platforms=['any'],
    command_options={
        'docs': {
            'version': ('setup.py', app.VERSION),
            'release': ('setup.py', app.VERSION)}
    },
    zip_safe=False,
    install_requires=[
        'uuid',
        'Django>=1.4.5',
    ],
    tests_require=[
    ],
    classifiers=[
        development_status,
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers'],
    long_description=open('README.rst').read()
)
