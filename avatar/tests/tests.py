from django.test import TestCase


class CategoryTest(TestCase):
    def test_save(self):
        pass


class PartTest(TestCase):
    def test_manager_get_default(self):
        pass

    def test_set_as_default(self):
        pass


class AvatarTest(TestCase):
    def test_to_dict(self):
        pass

    def test_to_json(self):
        pass

    def test_set_default(self):
        pass

    def test_update_from_json(self):
        pass

    def test_get_pngs(self):
        pass

    def test_save(self):
        pass


class AdminViewTests(TestCase):
    def test_set_default_part(self):
        pass


class SettingsTest(TestCase):
    def tearDown(self):
        pass

    def test_categories_dir(self):
        pass

    def test_parts_thumbs_dir(self):
        pass

    def test_parts_images_dir(self):
        pass

    def test_pats_images_dir(self):
        pass

    def test_avatars_thumbs_dir(self):
        pass

    def test_avatars_images_dir(self):
        pass

    def test_image_prefix(self):
        pass

    def test_thumbnail_prefix(self):
        pass

    def test_default_thumbnail_rate(self):
        pass
