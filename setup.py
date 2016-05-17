#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

version = '0.11'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'v%s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

if sys.argv[-1] == 'readme':
    print(readme)
    sys.exit()

requirements = ['requests']

setup(
    name='pyphaxio',
    version=version,
    packages=find_packages(),
    test_suite='tests',
    install_requires=requirements,
    include_package_data=True,

    # metadata for upload to PyPI
    author='Joshua Fialkoff',
    author_email='joshua.fialkoff@setaris.com',
    description='Python client for Phaxio',
    long_description=readme,
    license='MIT License',
    keywords='python phaxio fax api',
    url='https://github.com/jfialkoff/pyphaxio',
)
