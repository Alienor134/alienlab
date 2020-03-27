import os
import sys

from setuptools import setup, Extension, find_packages

install_requires=[
	matplotlib,
	datetime,
	PyQt5]


s = setup(
    name='alienlab',
    version='0.0.1',
    #scripts=[],
    packages=find_packages(),
    author='Alienor Lahlou',
    author_email='alienor.lahlou@espci.org',
    description='Matplotlib personal use',
    long_description='',
    url = 'https://github.com/Alienor134/alienlab',
    install_requires=install_requires,
    include_package_data=True,
)
