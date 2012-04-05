try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.files.base import ContentFile
from django.test import TestCase


class AvatarTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_test_file(self):
        import os
        path_to_file = '%s' % os.getcwd()
        f = open(path_to_file, 'rb')
        file_to_upload = StringIO(f.read())
        file_to_upload = ContentFile(file_to_upload.getvalue())
        file_to_upload.name = f.name
        return file_to_upload

    def test_to_dict(self):
        pass

    def test_to_json(self):
        pass

    def test_from_json(self):
        pass
