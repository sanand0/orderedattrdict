#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as fp:
    long_description = fp.read()

setup(
    name='orderedattrdict',
    version='1.5',
    description='OrderedDict with attribute-style access',
    long_description=long_description,
    author='S Anand',
    author_email='root.node@gmail.com',
    license='MIT',
    keywords='ordereddict ordered map attrdict tree conf config configuration yaml json',
    url='https://github.com/sanand0/orderedattrdict',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',    # For collections.OrderedDict
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite='tests',
    tests_require=['PyYAML'],
)
