#!/usr/bin/env python

# See https://packaging.python.org/en/latest/distributing.html
#   python3 setup.py sdist bdist_wheel --universal
#   twine upload dist/*

import io
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orderedattrdict',
    version='1.0.0',
    description='OrderedDict with attribute-style access',
    long_description=long_description,
    author='S Anand',
    author_email='root.node@gmail.com',
    license='MIT',
    keywords='ordereddict ordered map attrdict conf config configuration yaml json',
    url='https://github.com/sanand0/orderedattrdict',
    packages=find_packages(exclude=['tests*']),
    extras_require={
        'test': ['PyYAML'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',    # For OrderedDict
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
