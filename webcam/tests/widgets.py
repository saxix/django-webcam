# -*- coding: utf-8 -*-
import os
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import mock
import base64 as b64
from django.test import TestCase
from django.forms.models import modelform_factory
from webcam.picture import PictureUploadedFile
from webcam.storage import get_picture_name
from webcam.tests import temp_storage

from webcam.tests.models import FSDemoModel
from webcam.tests.util import PICTURE, PICTURE_PATH


cursor_wrapper = mock.Mock()
cursor_wrapper.side_effect = RuntimeError("No touching the database!")


# @mock.patch("django.db.backends.util.CursorWrapper", cursor_wrapper)
class WidgetTest(TestCase):
    def setUp(self):
        super(WidgetTest, self).setUp()

    def test_form_add(self):
        base64_picture_mime = b64.encodestring(PICTURE)
        Form = modelform_factory(FSDemoModel)

        form = Form({'data_photo': base64_picture_mime})
        assert form.is_valid(), form._errors
        obj = form.save()
        self.assertTrue(os.path.isfile(temp_storage.path(obj.photo.name)), '`{0.photo.name}` is not a file'.format(obj))
        self.assertEqual(len(obj.photo), File(file(PICTURE_PATH)).size)
        self.assertEqual(obj.photo.dimension, (320, 200))
        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertEqual(obj.photo.image.format, 'JPEG')

    def test_form_edit_no_data(self):
        obj = FSDemoModel(photo=SimpleUploadedFile('-1', PICTURE))
        obj.save()
        prev_name = obj.photo
        Form = modelform_factory(FSDemoModel)
        form = Form({}, instance=obj)
        assert form.is_valid(), form._errors
        obj = form.save()
        self.assertTrue(temp_storage.exists(obj.photo))
        self.assertEqual(prev_name, obj.photo)

    def test_edit_no_changes(self):

        base64_picture_mime = b64.encodestring(PICTURE)
        obj = FSDemoModel(photo=PictureUploadedFile(get_picture_name(), PICTURE))
        obj.save()
        obj = FSDemoModel.objects.get(pk=obj.pk)
        prev_name = obj.photo
        Form = modelform_factory(FSDemoModel)
        form = Form({'data_photo': base64_picture_mime}, instance=obj)
        obj = form.save()
        self.assertTrue(os.path.isfile(temp_storage.path(obj.photo.name)), '`{0.photo.name}` is not a file'.format(obj))
        self.assertEqual(prev_name, obj.photo)
        #
        self.assertEqual(obj.photo.dimension, (320, 200))
        self.assertEqual(len(obj.photo), File(file(PICTURE_PATH)).size)
        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertEqual(obj.photo.image.format, 'JPEG')

    # def test_form_not_valid(self):
    #     base64_picture_mime = b64.encodestring('123')
    #     Form = modelform_factory(FSDemoModel)
    #     form = Form({'photo': base64_picture_mime})
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual('* Not valid image', form.errors['photo'].as_text())
