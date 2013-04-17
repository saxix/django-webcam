# # -*- coding: utf-8 -*-
# import os
# from django.test import TestCase
# import mock
# import base64 as b64
# from scripttest import TestFileEnvironment
# from webcam.picture import CameraPicture
# from webcam.tests.util import mktree, is_jpg, PICTURE
#
# cursor_wrapper = mock.Mock()
# cursor_wrapper.side_effect = RuntimeError("No touching the database!")
#
# base = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, '~build', 'test-output'))
# mktree(os.path.dirname(base))
# fsenv = TestFileEnvironment(base, capture_temp=True, ignore_paths=['images'])
#
# class MockField(mock.Mock())
#
# @mock.patch("django.db.backends.util.CursorWrapper", cursor_wrapper)
# class CameraPictureTest(TestCase):
#
#     def setUp(self):
#         super(CameraPictureTest, self).setUp()
#
#     def test_stream_create(self):
#         base64_picture = b64.encodestring(PICTURE)
#         t = CameraPicture(None, , None, stream=base64_picture)
#         assert is_jpg(t.file)
#
#     def test_validate_success(self):
#         base64_picture = b64.encodestring(PICTURE)
#         t = CameraPicture(None, None, None, stream=base64_picture)
#         assert t.image
#
#     def test_validate_fail(self):
#         t = CameraPicture(None, None, None, stream='123')
#         assert not t.image
