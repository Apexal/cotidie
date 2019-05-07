#! /usr/bin/env python3

from setuptools import setup

setup(
    name='cotidie',
    packages=['cotidie'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy'
    ],
)