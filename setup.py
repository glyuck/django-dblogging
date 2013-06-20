#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-dblogging',
    version='.'.join(map(str, __import__('dblogging').__version__)),
    author='Vladimir Lyukov',
    author_email='v.lyukov@gmail.com',
    url='http://github.com/glyuck/django-dblogging',
    description = 'Logging to a Database for Django',
    packages=find_packages(),
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'django-appconf >= 0.4',
    ],
)