#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'girder>=3.0.0a2',
    'girder-jobs>=3.0.0a2',
    'girder-worker',
    'girder-worker-utils',
    'numpy',
    'netCDF4'
]

setup(
    author="Jonathan Beezley",
    author_email='jonathan.beezley@kitware.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    description='A plugin to parse and organize historical NARR surface temperature data',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description=readme,
    include_package_data=True,
    keywords='girder-plugin, sfc',
    name='girder_narr_sfc',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/girder_narr_sfc',
    version='0.1.0',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'sfc = girder_narr_sfc:GirderPlugin'
        ],
        'girder_worker_plugins': [
            'narr = girder_narr_sfc.GWPlugin'
        ]
    }
)
