import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='SNR',
    version='0.6.1',
    author='Spencer Shaw',
    author_email='calpolyroboticsclub@gmail.com',
    packages=find_packages(include=['snr']),
    url='http://github.com/sfshaw-calpoly/SNR',
    license='LICENSE.txt',
    description='Soft-realtime robotics framework for education',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'dataclasses;python_version<"3.7"',         # Dataclasses backport
        'dataclasses_json>=0.5.2',                  # Serialization
        # 'numpy>=1.20.0',                            # Kalman filter, CV
        # 'pygame>=2.0.0'                             # Controller
        'pyserial>=3.5',                            # Serial connection
        # 'pysimplegui=4.29.0',                       # GUI
    ],
    extras_require={
        'package': [
            'pip>=21.0',
            'setuptools',
            'wheel',
        ],
        'docs': 'pdoc>=6.1',    # Doc generation
        'test': [
            'pytest',           # Type checking
            'pytest-timeout',   # Test timeout
        ],
        'mypy': [
            'mypy>=0.800',      # Type checking
        ],
        'lint': [
            'flake8>=3.8',      # Linter
        ],
    },
    python_requires='>=3.7'
)
