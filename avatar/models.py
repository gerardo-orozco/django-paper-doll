import Image
import json
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


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


CATEGORIES_DIR = getattr(settings, 'CATEGORIES_DIR', category_upload_path)
PARTS_THUMBS_DIR = getattr(settings, 'PARTS_THUMBS_DIR', part_thumbnail_upload_path)
PARTS_IMAGES_DIR = getattr(settings, 'PARTS_IMAGES_DIR', part_image_upload_path)
AVATARS_THUMBS_DIR = getattr(settings, 'AVATARS_THUMBS_DIR', avatar_thumbnail_upload_path)
AVATARS_IMAGES_DIR = getattr(settings, 'AVATARS_IMAGES_DIR', avatar_image_upload_path)


class Category(models.Model):
    label = models.CharField(_(u'label'), max_length=50)
    display = models.CharField(_(u'display'), max_length=50, null=True)
    description = models.CharField(_(u'description'), max_length=100, null=True, blank=True)
    required = models.BooleanField(_(u'is required'), default=False)
    thumbnail = models.ImageField(_(u'thumbnail'), upload_to=CATEGORIES_DIR, blank=True, null=True)
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


class Part(models.Model):
    category = models.ForeignKey(Category, related_name='parts', verbose_name=_(u'category'))
    label = models.CharField(_(u'label'), max_length=30)
    display = models.CharField(_(u'display'), max_length=50, null=True)
    thumbnail = models.ImageField(_(u'thumbnail'), upload_to=PARTS_THUMBS_DIR, blank=True, null=True)
    image = models.ImageField(upload_to=PARTS_IMAGES_DIR)

    def __unicode__(self):
        return u'({category}) {name}'.format(category=self.category, name=self.display)

    class Meta:
        verbose_name = _(u'part')
        verbose_name_plural = _(u'parts')
        ordering = ('category__layer_index',)


class Avatar(models.Model):
    parts = models.ManyToManyField(Part, related_name='avatars', blank=True, null=True)
    thumbnail = models.ImageField(upload_to=AVATARS_THUMBS_DIR, blank=True, null=True)
    image = models.ImageField(upload_to=AVATARS_IMAGES_DIR, blank=True, null=True)

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

    def from_json(self, json):
        """
        Uses the given JSON to update the parts the Avatar image is built from.
        """
        parts = {}

        # Clean up parts so we don't save two or more parts of one category.
        for part_pk in json.values():
            try:
                part = Part.objects.get(pk=part_pk)
            except Part.DoesNotExist as e:
                e.message = 'Part object with pk={pk} does not exist.'.format(pk=part_pk)
                raise e

            category = part.category.label
            parts[category] = part

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
            rate = 0.2
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
            image.name = 'avatar_{pk}.png'.format(pk=self.pk)
            thumbnail.name = 'avatar_{pk}.png'.format(pk=self.pk)
            self.image = image
            self.thumbnail = thumbnail
        super(Avatar, self).save(*args, **kwargs)
