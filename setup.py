#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
import sys

from setuptools import setup, find_packages
import codecs
import os
import re


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
]

tests_require = [
    'nose',
]

setup(
    name='trigger',
    version=find_version("trigger", "__init__.py"),
    url='https://github.com/weiwongfaye/python_cli_template',
    license='MIT',
    author='jackw',
    author_email='weiwongfaye@hotmail.com',
    description='PYTHON cli template',
    scripts=['bin/trigger'],
    classifiers=[
        "Programming Language :: Python",
    ],
    platforms='any',
    keywords='splunk clustering docker',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
)