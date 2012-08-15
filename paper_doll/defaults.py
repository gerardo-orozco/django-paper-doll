# Default values and functions
from datetime import datetime
import hashlib
from django.conf import settings

DEFAULT_THUMBNAIL_RATE = 0.2
DEFAULT_DIGEST_LENGTH = 32
ADMIN_DEFAULT_IMAGE_RATE = 1
ADMIN_DEFAULT_THUMB_RATE = 1


def category_upload_path(instance, filename):
    return '/'.join(['categories', filename])


def part_thumbnail_upload_path(instance, filename):
    return '/'.join(['parts', 'thumbnails', instance.category.label, filename])


def part_image_upload_path(instance, filename):
    return '/'.join(['parts', 'images', instance.category.label, filename])


def avatar_thumbnail_upload_path(instance, filename):
    return '/'.join(['avatars', 'thumbnails', filename])


def avatar_image_upload_path(instance, filename):
    return '/'.join(['avatars', 'images', filename])


def avatar_image_name_format(instance):
    # May support more formats later, forcing PNG for now
    return instance.digest


def avatar_thumbnail_name_format(instance):
    # May support more formats later, forcing PNG for now
    return 'thumb_{}'.format(instance.digest)


def avatar_digester(instance):
    limit = getattr(settings, 'PAPER_DOLL_DIGEST_LENGTH', DEFAULT_DIGEST_LENGTH)
    content = '%s%s' % (instance.pk, datetime.now())
    digest = hashlib.sha1(content)
    return digest.hexdigest()[:limit]
