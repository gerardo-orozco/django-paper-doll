#!/usr/bin/env python
import os
from avatar import version
from setuptools import setup


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('avatar'):
        if '__init__.py' in filenames:
            packages.append('.'.join(os.path.split(root)).strip('.'))

    return packages

requires = ['PIL==1.1.6']

setup(name='django-custom-avatar',
    version=version,
    description='A Django App that helps creating customizable avatar images.',
    author=u'Gerardo Orozco Mosqueda',
    author_email='gerardo.orozcom.mosqueda@gmail.com',
    url='https://github.com/gerardo-orozco/django-custom-avatar',
    packages=get_packages(),
    install_requires=requires,
)
