from setuptools import find_packages
from setuptools import setup

VERSION = '0.0.2'

setup(
    name='gaeutils',
    version=VERSION,
    description='Useful utilities for working with Google App Engine',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    maintainer='Tyler Treat',
    url='https://github.com/tylertreat/gaeutils',
    maintainer_email='ttreat31@gmail.com'
)

