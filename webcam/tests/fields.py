import tempfile
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.core.files.storage import FileSystemStorage
from webcam.tests.models import FSDemoModel
from django.core.cache import cache

temp_storage_location = tempfile.mkdtemp(prefix='_webcam')
temp_storage = FileSystemStorage(location=temp_storage_location)


class FieldTest(TestCase):

    def test_create_save(self):
        temp_storage.save('tests/default.txt', ContentFile('default content'))
        self.assertRaises(AttributeError, lambda: FSDemoModel.photo)

        d = FSDemoModel.objects.create()
        self.assertFalse(d.photo)

    def test_files(self):
        temp_storage.save('tests/default.txt', ContentFile('default content'))
        # Attempting to access a FileField from the class raises a descriptive
        # error
        self.assertRaises(AttributeError, lambda: FSDemoModel.photo)

        # An object without a file has limited functionality.
        obj1 = FSDemoModel()
        self.assertEqual(obj1.photo.name, "")
        self.assertRaises(ValueError, lambda: obj1.photo.size)

        # Saving a file enables full functionality.
        obj1.photo.save("django_test.txt", ContentFile("content"))

        self.assertEqual(obj1.photo.name, "tests/django_test.txt")
        self.assertEqual(obj1.photo.size, 7)
        self.assertEqual(obj1.photo.read(), "content")
        # self.assertFalse(lambda : obj1.photo.is_valid())
        obj1.photo.close()

        # File objects can be assigned to FileField attributes, but shouldn't
        # get committed until the model it's attached to is saved.
        obj1.photo = SimpleUploadedFile("assignment.txt", "content")
        dirs, files = temp_storage.listdir("tests")
        self.assertEqual(dirs, [])
        self.assertEqual(sorted(files), ["default.txt", "default_1.txt"])

        # obj1.save()
        # dirs, files = temp_storage.listdir("tests")
        # self.assertEqual(
        #     sorted(files), ["assignment.txt", "default.txt", "django_test.txt"]
        # )

        # Files can be read in a little at a time, if necessary.
        obj1.photo.open()
        self.assertEqual(obj1.photo.read(3), "con")
        self.assertEqual(obj1.photo.read(), "tent")
        self.assertEqual(list(obj1.photo.chunks(chunk_size=2)), ["co", "nt", "en", "t"])
        obj1.photo.close()

        # Save another file with the same name.
        obj2 = FSDemoModel()
        obj2.photo.save("django_test.txt", ContentFile("more content"))
        self.assertEqual(obj2.photo.name, "tests/django_test_1.txt")
        self.assertEqual(obj2.photo.size, 12)

        # Push the objects into the cache to make sure they pickle properly
        cache.set("obj1", obj1)
        cache.set("obj2", obj2)
        self.assertEqual(cache.get("obj2").photo.name, "tests/django_test_1.txt")

        # Deleting an object does not delete the file it uses.
        obj2.delete()
        obj2.photo.save("django_test.txt", ContentFile("more content"))
        self.assertEqual(obj2.photo.name, "tests/django_test_2.txt")

        # Multiple files with the same name get _N appended to them.
        objs = [FSDemoModel() for i in range(3)]
        for o in objs:
            o.photo.save("multiple_files.txt", ContentFile("Same Content"))
        self.assertEqual(
            [o.photo.name for o in objs],
            ["tests/multiple_files.txt", "tests/multiple_files_1.txt", "tests/multiple_files_2.txt"]
        )
        for o in objs:
            o.delete()

        # Default values allow an object to access a single file.
        # obj3 = FSDemoModel.objects.create()
        # self.assertEqual(obj3.default.name, "tests/default.txt")
        # self.assertEqual(obj3.default.read(), "default content")
        # obj3.default.close()

        # But it shouldn't be deleted, even if there are no more objects using
        # it.
        # obj3.delete()
        # obj3 = FSDemoModel()
        # self.assertEqual(obj3.default.read(), "default content")
        # obj3.default.close()

        # Verify the fix for #5655, making sure the directory is only
        # determined once.
        # obj4 = FSDemoModel()
        # obj4.random.save("random_file", ContentFile("random content"))
        # self.assertTrue(obj4.random.name.endswith("/random_file"))

        # Clean up the temporary files and dir.
        obj1.photo.delete()
        # obj2.photo.delete()
        # obj3.default.delete()
        # obj4.random.delete()

#         d = FSDemoModel.objects.get(pk=d.pk)
#         self.assertTrue(isinstance(d.photo, CameraPicture))
#         self.assertFalse(d.photo)
#         #
#         # d = DataModel.objects.defer("data").get(pk=d.pk)
#         # d.save()
#         #
#         # d = DataModel.objects.get(pk=d.pk)
#         # self.assertTrue(isinstance(d.data, list))
#         # self.assertEqual(d.data, [1, 2, 3])
# #
