import os
import sys

from setuptools import setup, Extension, find_packages

install_requires=[
	'matplotlib>=3.2.1',
	'DateTime',
	'opencv-python>=4.2.0.34',
	'labelme>= 4.2.10',
	'imageio>= 2.8.0',
	'scikit-image>= 0.16.2',
	'joblib>= 0.14.1',
	'pillow>= 7.1.1',
	'imgviz>= 0.11.0', 
	'pandas', 
    'colorlog',
    'statsmodels', 
    'scipy']

#and PyQt5


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
