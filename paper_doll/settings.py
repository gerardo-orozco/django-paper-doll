# Settings to be overriden by project settings
from django.conf import settings
from paper_doll.defaults import (
    # default values
    DEFAULT_THUMBNAIL_RATE,
    DEFAULT_DIGEST_LENGTH,
    ADMIN_DEFAULT_IMAGE_RATE,
    ADMIN_DEFAULT_THUMB_RATE,
    # default functions
    category_upload_path,
    part_thumbnail_upload_path,
    part_image_upload_path,
    avatar_thumbnail_upload_path,
    avatar_image_upload_path,
    avatar_image_name_format,
    avatar_thumbnail_name_format,
    avatar_digester,
)

# Models Settings  ############################################################
PAPER_DOLL_CATEGORIES_DIR = getattr(settings, 'CATEGORIES_DIR',
                                category_upload_path)
PAPER_DOLL_PARTS_THUMBS_DIR = getattr(settings, 'PARTS_THUMBS_DIR',
                                  part_thumbnail_upload_path)
PAPER_DOLL_PARTS_IMAGES_DIR = getattr(settings, 'PARTS_IMAGES_DIR',
                                  part_image_upload_path)
PAPER_DOLL_AVATARS_THUMBS_DIR = getattr(settings, 'AVATARS_THUMBS_DIR',
                                    avatar_thumbnail_upload_path)
PAPER_DOLL_AVATARS_IMAGES_DIR = getattr(settings, 'AVATARS_IMAGES_DIR',
                                    avatar_image_upload_path)
PAPER_DOLL_IMAGE_NAME_FORMATTER = getattr(settings, 'PAPER_DOLL_IMAGE_NAME_FORMATTER',
                                      avatar_image_name_format)
PAPER_DOLL_THUMBNAIL_NAME_FORMATTER = getattr(settings,
                                          'PAPER_DOLL_THUMBNAIL_NAME_FORMATTER',
                                          avatar_thumbnail_name_format)
PAPER_DOLL_DIGEST_LENGTH = getattr(settings, 'PAPER_DOLL_DIGEST_LENGTH',
                               DEFAULT_DIGEST_LENGTH)
PAPER_DOLL_DIGESTER = getattr(settings, 'PAPER_DOLL_DIGESTER', avatar_digester)
PAPER_DOLL_DEFAULT_THUMBNAIL_RATE = getattr(settings,
                                        'PAPER_DOLL_DEFAULT_THUMBNAIL_RATE',
                                        DEFAULT_THUMBNAIL_RATE)


# Admin settings  #############################################################
# Percent rate of images being show in lists
PAPER_DOLL_ADMIN_IMAGE_RATE = getattr(settings, 'PAPER_DOLL_ADMIN_IMAGE_RATE',
                                      ADMIN_DEFAULT_IMAGE_RATE)
PAPER_DOLL_ADMIN_THUMB_RATE = getattr(settings, 'PAPER_DOLL_ADMIN_THUMB_RATE',
                                      ADMIN_DEFAULT_THUMB_RATE)
PAPER_DOLL_ADMIN_PAPER_DOLL_RATE = getattr(settings, 'PAPER_DOLL_ADMIN_PAPER_DOLL_RATE',
                                           PAPER_DOLL_ADMIN_IMAGE_RATE)
