from datetime import datetime
import hashlib
import json
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import Image
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Defaults
DEFAULT_THUMBNAIL_RATE = 0.2
DEFAULT_DIGEST_LENGTH = 32


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


def avatar_digester(instance):
    limit = getattr(settings, 'AVATAR_DIGEST_LENGTH', DEFAULT_DIGEST_LENGTH)
    content = '%s%s' % (instance.pk, datetime.now())
    digest = hashlib.sha1(content)
    return digest.hexdigest()[:limit]


def avatar_image_name_format(instance):
    # May support more formats later, forcing PNG for now
    return instance.digest


def avatar_thumbnail_name_format(instance):
    # May support more formats later, forcing PNG for now
    return 'thumb_{}'.format(instance.digest)


# Settings
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


# Actual models
class Category(models.Model):
    label = models.CharField(_(u'label'), max_length=50)
    display = models.CharField(_(u'display'), max_length=50, null=True)
    description = models.CharField(_(u'description'), max_length=100,
                                   null=True, blank=True)
    required = models.BooleanField(_(u'is required'), default=False)
    thumbnail = models.ImageField(_(u'thumbnail'),
                                    upload_to=AVATAR_CATEGORIES_DIR,
                                    blank=True, null=True)
    layer_index = models.PositiveIntegerField(_(u'layer index'), unique=True)

    def __unicode__(self):
        return self.display

    def save(self, *args, **kwargs):
        self.label = self.label.replace(' ', '_')
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')
        ordering = ('layer_index', 'label')


class PartManager(models.Manager):
    def get_default(self):
        parts = {}
        default_parts = self.filter(is_default=True)
        for part in default_parts:
            parts[part.category.label] = part
        return parts


class Part(models.Model):
    category = models.ForeignKey(Category, related_name='parts',
                                 verbose_name=_(u'category'))
    label = models.CharField(_(u'label (for in-app use)'), max_length=30)
    display = models.CharField(_(u'verbose name'), max_length=50, null=True)
    is_default = models.BooleanField(_(u'is_default'), default=False)
    thumbnail = models.ImageField(_(u'thumbnail'),
                                  upload_to=AVATAR_PARTS_THUMBS_DIR,
                                  blank=True, null=True)
    image = models.ImageField(upload_to=AVATAR_PARTS_IMAGES_DIR)

    objects = PartManager()

    def set_as_default(self, commit=True):
        """
        Sets the current Part as default for its Category so it gets
        automatically added to the avatar if no Part is given for such Category.
        """
        self.category.parts.update(is_default=False)
        self.is_default = True
        if commit:
            self.save()

    def __unicode__(self):
        return u'({0}) {1}'.format(self.category, self.display)

    class Meta:
        verbose_name = _(u'part')
        verbose_name_plural = _(u'parts')
        ordering = ('category__layer_index', 'label')


class Avatar(models.Model):
    parts = models.ManyToManyField(Part, related_name='avatars', blank=True,
                                   null=True)
    thumbnail = models.ImageField(upload_to=AVATAR_AVATARS_THUMBS_DIR,
                                  blank=True, null=True)
    image = models.ImageField(upload_to=AVATAR_AVATARS_IMAGES_DIR, blank=True,
                              null=True)
    digest = models.CharField(max_length=AVATAR_DIGEST_LENGTH)

    def to_dict(self):
        """
        Organizes the parts of the current Avatar in a dictionary for
        easy manipulation.
        """
        parts = {}
        for part in self.parts.all():
            category = part.category.label
            parts[category] = {'pk': part.pk, 'src': part.image.url}
        return parts

    def to_json(self):
        """
        Parses the parts of the current Avatar to a JSON string
        for further use in front-end.
        """
        return json.dumps(self.to_dict())

    def set_default(self, current_parts):
        """
        Sets the default part for each category set in settings if no part
        was set for such categories.
        """
        default_parts = Part.objects.get_default()
        for category, part in default_parts.iteritems():
            if not category in current_parts:
                current_parts[category] = part

    def update(self, json_or_dict):
        """
        Uses the given JSON to update the parts the Avatar image is built from.
        """
        if not isinstance(json_or_dict, dict):
            try:
                json_or_dict = json.loads(json_or_dict)
            except TypeError as e:
                e.message = 'Please use a JSON-like string or a dictionary'
                raise e
        parts = {}

        # Clean up parts so we don't save two or more parts of one category.
        for part_pk in json_or_dict.values():
            try:
                part = Part.objects.get(pk=part_pk)
            except Part.DoesNotExist as e:
                e.message = 'Part with pk={} does not exist.'.format(part_pk)
                raise e

            category = part.category.label
            parts[category] = part
            self.set_default(parts)

        self.parts = parts.values()

    def get_pngs(self, thumb_size=None):
        """
        Builds the Avatar image from the images associated to each part
        related to the `Avatar` object.
        """
        parts = self.parts.all()
        base = parts.pop(0)
        base = Image.open(StringIO(base.image.read()))
        for part in parts:
            buffer_ = StringIO(part.image.read())
            image = Image.open(buffer_)
            base.paste(image, image)

        # Create the main image
        image = StringIO()
        base.save(image, 'PNG')
        image = ContentFile(image.getvalue())

        # Create the thumbnail
        size = thumb_size
        if not thumb_size:
            rate = AVATAR_DEFAULT_THUMBNAIL_RATE
            size = base.size
            size = (int(size[0] * rate), int(size[1] * rate))
        base.thumbnail(size)
        thumbnail = StringIO()
        base.save(thumbnail, 'PNG')
        thumbnail = ContentFile(thumbnail.getvalue())

        return (image, thumbnail)

    def save(self, thumb_size=None, *args, **kwargs):
        if self.pk:
            image, thumbnail = self.get_pngs(thumb_size=thumb_size)

            self.digest = AVATAR_DIGESTER(self)
            # format main image name
            image_formatter = AVATAR_IMAGE_NAME_FORMATTER
            image_name = image_formatter(self)
            image.name = '{}.png'.format(image_name)

            # format thumbnail image name
            thumbnail_formatter = AVATAR_THUMBNAIL_NAME_FORMATTER
            thumbnail_name = thumbnail_formatter(self)
            thumbnail.name = '{}.png'.format(thumbnail_name)

            self.image = image
            self.thumbnail = thumbnail

        super(Avatar, self).save(*args, **kwargs)
