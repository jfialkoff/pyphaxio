from setuptools import setup, find_packages

setup(
    name='pyphaxio',
    version='0.9',
    packages=find_packages(),
    test_suite='tests',
    install_requires=['requests'],
    include_package_data=True,

    # metadata for upload to PyPI
    author='Joshua Fialkoff',
    author_email='joshua.fialkoff@setaris.com',
    description='Python client for Phaxio',
    license='MIT License',
    keywords='python phaxio fax',
    url='https://github.com/setaris/pyphaxio',
)
