import pathlib

from setuptools import find_packages, setup

import project_requires

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='SNR',
    version='0.5.1',
    author='Spencer Shaw',
    author_email='calpolyroboticsclub@gmail.com',
    packages=find_packages(include=['snr']),
    url='http://github.com/sfshaw-calpoly/SNR',
    license='LICENSE.txt',
    description='Soft-realtime robotics framework for education',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=project_requires.install_deps,
    extras_require={
        'package': [
            'pip>=21.0',
            'setuptools',
            'wheel',
        ],
        'docs': project_requires.docs_deps,
        'test': 'nox',
    },
    python_requires='>=3.6.12'
)
