# -*- coding: utf-8 -*-
import os
import base64 as b64
from django.core.files.uploadedfile import File, SimpleUploadedFile
from django.test import TestCase
from django.forms.models import modelform_factory
from webcam.picture import PictureUploadedFile
from webcam.storage import get_picture_name
from webcam.tests import temp_storage

from webcam.tests.models import WebcamTestModel
from webcam.tests.util import PICTURE, PICTURE_PATH


class WidgetTest(TestCase):
    def setUp(self):
        super(WidgetTest, self).setUp()

    def test_form_add(self):
        base64_picture_mime = b64.encodestring(PICTURE)
        Form = modelform_factory(WebcamTestModel)

        form = Form({'data_photo': base64_picture_mime})
        assert form.is_valid(), form._errors
        obj = form.save()

        self.assertTrue(os.path.isfile(temp_storage.path(obj.photo.name)), '`{0.photo.name}` is not a file'.format(obj))
        self.assertEqual(len(obj.photo), File(file(PICTURE_PATH)).size)

    def test_form_edit_no_data(self):
        obj = WebcamTestModel(photo=SimpleUploadedFile('-1', PICTURE))
        obj.save()
        prev_name = obj.photo
        Form = modelform_factory(WebcamTestModel)
        form = Form({}, instance=obj)
        assert form.is_valid(), form._errors
        obj = form.save()

        self.assertTrue(os.path.isfile(temp_storage.path(obj.photo)), '`{0.photo.name}` is not a file'.format(obj))
        self.assertEqual(prev_name, obj.photo)

    def test_edit_no_changes(self):

        base64_picture_mime = b64.encodestring(PICTURE)
        obj = WebcamTestModel(photo=PictureUploadedFile(get_picture_name(), PICTURE))
        obj.save()
        obj = WebcamTestModel.objects.get(pk=obj.pk)
        prev_name = obj.photo
        Form = modelform_factory(WebcamTestModel)
        form = Form({'data_photo': base64_picture_mime}, instance=obj)
        obj = form.save()

        self.assertTrue(os.path.isfile(temp_storage.path(obj.photo.name)), '`{0.photo.name}` is not a file'.format(obj))
        self.assertEqual(prev_name, obj.photo)
