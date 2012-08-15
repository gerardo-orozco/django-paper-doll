# Settings to be overriden by project settings
from django.conf import settings
from avatar.defaults import (
    DEFAULT_THUMBNAIL_RATE,
    DEFAULT_DIGEST_LENGTH,
    category_upload_path,
    part_thumbnail_upload_path,
    part_image_upload_path,
    avatar_thumbnail_upload_path,
    avatar_image_upload_path,
    avatar_image_name_format,
    avatar_thumbnail_name_format,
    avatar_digester,
)


AVATAR_CATEGORIES_DIR = getattr(settings, 'CATEGORIES_DIR',
                                category_upload_path)
AVATAR_PARTS_THUMBS_DIR = getattr(settings, 'PARTS_THUMBS_DIR',
                                  part_thumbnail_upload_path)
AVATAR_PARTS_IMAGES_DIR = getattr(settings, 'PARTS_IMAGES_DIR',
                                  part_image_upload_path)
AVATAR_AVATARS_THUMBS_DIR = getattr(settings, 'AVATARS_THUMBS_DIR',
                                    avatar_thumbnail_upload_path)
AVATAR_AVATARS_IMAGES_DIR = getattr(settings, 'AVATARS_IMAGES_DIR',
                                    avatar_image_upload_path)
AVATAR_IMAGE_NAME_FORMATTER = getattr(settings, 'AVATAR_IMAGE_NAME_FORMATTER',
                                      avatar_image_name_format)
AVATAR_THUMBNAIL_NAME_FORMATTER = getattr(settings,
                                          'AVATAR_THUMBNAIL_NAME_FORMATTER',
                                          avatar_thumbnail_name_format)
AVATAR_DIGEST_LENGTH = getattr(settings, 'AVATAR_DIGEST_LENGTH',
                               DEFAULT_DIGEST_LENGTH)
AVATAR_DIGESTER = getattr(settings, 'AVATAR_DIGESTER', avatar_digester)
AVATAR_DEFAULT_THUMBNAIL_RATE = getattr(settings,
                                        'AVATAR_DEFAULT_THUMBNAIL_RATE',
                                        DEFAULT_THUMBNAIL_RATE)
