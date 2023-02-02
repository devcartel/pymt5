#!/usr/bin/python
from setuptools import setup, find_packages
from setuptools.dist import Distribution
# To use a consistent encoding
from codecs import open
from os import path
import platform

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pymt5',
    version='1.4.0',
    description='Python API for MetaTrader 5 gateways',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devcartel/pymt5',
    author='DevCartel',
    author_email='support@devcartel.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='metatrader, metaquotes, mt5, gateway, api, python',
    packages=['pymt5']
)
