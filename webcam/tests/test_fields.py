# -*- coding: utf-8 -*-
import os
import re
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from unittest import skipIf
import sys
from webcam.tests import temp_storage, PICTURE
from webcam.tests.models import WebcamTestModel
from django.core.cache import cache
from webcam.tests.util import rmtree

uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
uuid_rex = re.compile(uuid_pattern, re.IGNORECASE)


class FieldTest(TestCase):
    def setUp(self):
        super(FieldTest, self).setUp()
        rmtree(temp_storage.base_location)

    def tearDown(self):
        super(FieldTest, self).tearDown()
        rmtree(temp_storage.base_location)

    def test_create_save(self):
        temp_storage.save('tests/default.jpg', ContentFile(PICTURE))
        self.assertRaises(AttributeError, lambda: WebcamTestModel.photo)

        d = WebcamTestModel.objects.create()
        self.assertFalse(d.photo)

    @skipIf(not 'PIL' in sys.modules, "PIL not installed")
    def test_image(self):
        obj = WebcamTestModel()
        obj.photo = SimpleUploadedFile("assignment.jpg", PICTURE)
        obj.save()

        self.assertEqual(obj.photo.dimension, (320, 200))

        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertEqual(obj.photo.image.format, 'JPEG')

    def test_files(self):
        temp_storage.save('tests/default.jpg', ContentFile(PICTURE))
        # Attempting to access a FileField from the class raises a descriptive
        # error
        self.assertRaises(AttributeError, lambda: WebcamTestModel.photo)

        # An object without a file has limited functionality.
        obj1 = WebcamTestModel()
        self.assertEqual(obj1.photo.name, None)
        self.assertRaises(ValueError, lambda: obj1.photo.size)

        # Saving a file enables full functionality.
        # self.assertRaises(ValueError, obj1.photo.save, "django_test.txt", ContentFile("content"))

        obj1.photo.save(None, ContentFile(PICTURE))
        filename = os.path.basename(obj1.photo.name)

        basename, suffix = filename.split('.')
        self.assertTrue(temp_storage.exists(obj1.photo.name), filename)
        self.assertTrue(uuid_rex.match(basename))
        self.assertEqual(obj1.photo.size, 53472)
        self.assertTrue(lambda: obj1.photo.is_valid())
        obj1.photo.close()

        # File objects can be assigned to FileField attributes, but shouldn't
        # get committed until the model it's attached to is saved.
        obj1.photo = SimpleUploadedFile("assignment.jpg", PICTURE)
        dirs, files = temp_storage.listdir("tests")
        self.assertEqual(dirs, [])
        # self.assertEqual(sorted(files), sorted(["default.jpg", filename]))

        obj1.save()
        self.assertEqual(str(obj1.photo), "tests/assignment.jpg")
        dirs, files = temp_storage.listdir("tests")
        self.assertEqual(
            sorted(files), sorted(["assignment.jpg", "default.jpg", filename])
        )

        # Files can be read in a little at a time, if necessary.
        obj1.photo.open()
        self.assertEqual(obj1.photo.read(3), PICTURE[:3])
        obj1.photo.close()

        obj2 = WebcamTestModel()
        obj2.photo.save("assignment.txt", ContentFile(PICTURE))

        # Push the objects into the cache to make sure they pickle properly
        cache.set("obj1", obj1)
        cache.set("obj2", obj2)

        self.assertEqual(cache.get("obj2").photo.name, "tests/assignment.txt")

        # Deleting an object does not delete the file it uses.
        obj2.delete()
        obj2.photo.save("django_test.txt", ContentFile(PICTURE))
        self.assertEqual(obj2.photo.name, "tests/django_test.txt")
