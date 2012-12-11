import shutil
import tempfile
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.forms.models import modelform_factory
from django.test import TestCase
from django.test.utils import override_settings
import base64 as b64
import os
from webcam.utils import InvalidImageFormat, Base64Image
from webcam.tests.models import DBDemoModel, FSDemoModel


APPS = ['webcam.tests'] + list(settings.INSTALLED_APPS)


def override_app():
    return override_settings(INSTALLED_APPS=APPS, MEDIA_ROOT=tempfile.gettempdir())

HERE = os.path.dirname(__file__)
PICTURE_NAME = 'colosseo.jpg'
PICTURE_PATH = os.path.join(HERE, 'data', PICTURE_NAME)
PICTURE = file(PICTURE_PATH).read()


class CameraFieldTest(TestCase):
    def _pre_setup(self):
        with self.settings(INSTALLED_APPS=APPS):
            from django.core.management import call_command
            from django.db.models import loading

            loading.cache.loaded = False
            call_command('syncdb', verbosity=0)
        super(CameraFieldTest, self)._pre_setup()


class TestDBCameraField(CameraFieldTest):
    @override_app()
    def test_database(self):
        base64_picture = b64.encodestring(PICTURE)
        obj = DBDemoModel.objects.create(photo=Base64Image(base64_picture))
        obj.save()
        obj = DBDemoModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.photo.size, 53472)
        self.assertEqual(len(obj.photo), 72235)
        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertTrue(obj.photo.image)

    @override_app()
    def test_empty_field(self):
        obj = DBDemoModel()
        obj.save()
        self.assertFalse(obj.photo)
        self.assertRaises(InvalidImageFormat, lambda: obj.photo.size)
        self.assertRaises(InvalidImageFormat, lambda: obj.photo.width)
        self.assertRaises(InvalidImageFormat, lambda: obj.photo.height)
        self.assertRaises(InvalidImageFormat, lambda: obj.photo.image)

    @override_app()
    def test_empty_save(self):
        obj = DBDemoModel()
        obj.save()
        obj = DBDemoModel.objects.get(pk=obj.pk)
        self.assertFalse(obj.photo)
        self.assertRaises(InvalidImageFormat, lambda: obj.photo.size)

    @override_app()
    def test_wrong_value(self):
        obj = DBDemoModel(photo='aaaaaaaaa')
        self.assertRaises(InvalidImageFormat, lambda x: obj.photo.width, 0)
        self.assertRaises(InvalidImageFormat, lambda x: obj.photo.height, 0)
        self.assertRaises(InvalidImageFormat, lambda x: obj.photo.size, 0)

    @override_app()
    def test_form(self):
        base64_picture_mime = b64.encodestring(PICTURE)
        Form = modelform_factory(DBDemoModel)
        form = Form({'photo': base64_picture_mime})
        form.is_valid()
        obj = form.save()
        self.assertEqual(obj.photo.size, 53472)
        self.assertEqual(len(obj.photo), 72235)
        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertTrue(obj.photo.image)

    @override_app()
    def test_form_error(self):
        Form = modelform_factory(DBDemoModel)
        form = Form({'photo': 111})
        self.assertFalse(form.is_valid())

        form = Form({'photo': '111'})
        self.assertFalse(form.is_valid())


class TestFSCameraField(CameraFieldTest):
    def test_filesystem_create(self):
        shutil.copyfile(PICTURE_PATH, os.path.join(settings.MEDIA_ROOT, PICTURE_NAME))
        base64_picture = b64.encodestring(PICTURE)
        obj = FSDemoModel.objects.create(photo=Base64Image(base64_picture))

        obj.save()

        obj = FSDemoModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.photo.size, 53472)
        self.assertEqual(len(obj.photo), 72235)
        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertTrue(obj.photo.image)

    @override_app()
    def test_empty_field(self):
        obj = FSDemoModel()
        obj.save()
        self.assertFalse(obj.photo)
        self.assertRaises(InvalidImageFormat,lambda : obj.photo.size)
        self.assertRaises(InvalidImageFormat,lambda : obj.photo.width)
        self.assertRaises(InvalidImageFormat,lambda : obj.photo.height)
        self.assertRaises(InvalidImageFormat,lambda : obj.photo.image)

    @override_app()
    def test_wrong_value(self):
        obj = FSDemoModel(photo='aaaaaaaaa')
        self.assertRaises(IOError, lambda x: obj.photo.width, 0)
        self.assertRaises(IOError, lambda x: obj.photo.height, 0)
        self.assertRaises(IOError, lambda x: obj.photo.size, 0)
