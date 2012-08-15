import random
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import Image
from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.core.files.base import ContentFile
from django.utils.importlib import import_module
from avatar.models import Part, Category, Avatar


def login(request, user, backend='django.contrib.backends.ModelBackend'):
    engine = import_module(settings.SESSION_ENGINE)
    request.user = user
    request.session = engine.SessionStore()
    request.session[SESSION_KEY] = user.pk
    request.session[BACKEND_SESSION_KEY] = backend
    request.session.save()


def simple_factory(model, amount=1, save=False, *args, **kwargs):
    """ Simple instance factory for models """

    def _create_model_instance(**kwargs_):
        instance = model(*args, **kwargs_)
        if save:
            return instance.save()
        return instance

    instances = []
    for i in amount:
        instances.append(_create_model_instance(*args, **kwargs))

    if len(amount) == 1:
        return instances[0]
    return instances


def get_unique_label(length=10):
    letters = 'abcdefghijklmnopqrstuvwxyz1234567890_'
    return ''.join([random.choice(letters) for i in xrange(length)])


def test_image(format='PNG'):
    io = StringIO()
    size = (50, 50)
    color = (0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(io, format=format.upper())
    image_file = ContentFile(io.getvalue())
    image_file.name = 'test_image.%s' % format.lower()
    image_file.seek(0)
    return image_file


def CategoryFactory(save=False, *args, **kwargs):
    if not 'label' in kwargs:
        kwargs['label'] = get_unique_label()
    return simple_factory(Category, save=save, *args, **kwargs)


def PartFactory(amount=1, save=False, *args, **kwargs):
    if not 'category' in kwargs:
        kwargs['category'] = CategoryFactory()
    if not 'label' in kwargs:
        kwargs['label'] = get_unique_label()
    if not 'image' in kwargs:
        kwargs['image'] = test_image()
    return simple_factory(Part, amount=amount, save=save, *args, **kwargs)


def AvatarFactory(amount=1, save=False, *args, **kwargs):
    return simple_factory(Avatar, amount=amount, save=save, *args, **kwargs)
