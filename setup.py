from setuptools import setup, find_packages

setup(
    name='SNR',
    version='0.3.0',
    author='Spencer Shaw',
    author_email='sfshaw@calpoly.edu',
    packages=find_packages(),
    url='http://calpoly.edu',
    license='LICENSE.txt',
    description='Soft-realtime robotics framework for education',
    long_description=open('README.txt').read(),
    install_requires=[line for line in open("requirements.txt")],
)
