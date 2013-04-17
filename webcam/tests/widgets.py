# -*- coding: utf-8 -*-
import os
import mock
import base64 as b64
from django.test import TestCase
from django.forms.models import modelform_factory

from webcam.tests.models import FSDemoModel
from webcam.tests.util import mktree, PICTURE_PATH, PICTURE

from scripttest import TestFileEnvironment

cursor_wrapper = mock.Mock()
cursor_wrapper.side_effect = RuntimeError("No touching the database!")

base = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, '~build', 'test-output'))
mktree(os.path.dirname(base))
fsenv = TestFileEnvironment(base, capture_temp=True, ignore_paths=['images'])


# @mock.patch("django.db.backends.util.CursorWrapper", cursor_wrapper)
class WidgetTest(TestCase):
    def setUp(self):
        super(WidgetTest, self).setUp()

    def test_form(self):
        base64_picture_mime = b64.encodestring(PICTURE)
        Form = modelform_factory(FSDemoModel)
        form = Form({'photo': base64_picture_mime})
        assert form.is_valid(), form.errors
        obj = form.save()
        self.assertEqual(obj.photo.dimension, (320, 200))
        # self.assertEqual(len(obj.photo), File(file(PICTURE_PATH)).size)
        self.assertEqual(obj.photo.width, 320)
        self.assertEqual(obj.photo.height, 200)
        self.assertEqual(obj.photo.image.format, 'JPEG')

    # def test_form_not_valid(self):
    #     base64_picture_mime = b64.encodestring('123')
    #     Form = modelform_factory(FSDemoModel)
    #     form = Form({'photo': base64_picture_mime})
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual('* Not valid image', form.errors['photo'].as_text())
