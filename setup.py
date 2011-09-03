#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup, find_packages


if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "testing", "release.py")))


additional_requires = ['futures'] if sys.version_info < (3, 2) else []


setup(
        name = "marrow.testing",
        version = version,
        
        description = "Descriptive business logic testing.",
        long_description = """\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.testing""",
        
        author = "Alice Bevan-McGregor",
        author_email = "alice+marrow@gothcandy.com",
        url = "https://github.com/marrow/marrow.testing",
        license = "MIT",
        
        install_requires = [
            'marrow.util < 2.0',
        ] + additional_requires,
        
        test_suite = 'nose.collector',
        tests_require = [
            'nose',
            'coverage'
        ],
        
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        
        packages = find_packages(exclude=['examples', 'tests']),
        zip_safe = True,
        include_package_data = True,
        package_data = {'': ['README.textile', 'LICENSE']},
        
        namespace_packages = ['marrow'],
        
        entry_points = {
            'marrow.logging.filter': [
                #' = marrow.logging.filter.:',
            ],
            'marrow.logging.format': [
                #' = marrow.logging.format.:',
            ],
            'marrow.logging.transport': [
                #' = marrow.logging.transport.:',
            ]
        }
    )
