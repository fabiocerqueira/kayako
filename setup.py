# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the GNU General Public License (GPL)
#-----------------------------------------------------------------------------

from setuptools import setup, find_packages

with open('kayako/README.txt') as readme:
    long_description = readme.read()

setup(
    name='kayako',
    version='4.01.204',
    author='Evan Leis',
    author_email='engineergod@yahoo.com',
    url='',
    install_requires=[
        "lxml",
    ],
    setup_requires=[],
    packages=find_packages(exclude=[]),
    include_package_data=True,
    test_suite='kayako.tests',
    package_data={},
    zip_safe=True,
    entry_points="""
    """,
    license="GNU General Public License (GPL)",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Python API Wrapper for Kayako 4.01.204",
    long_description=long_description,
)
