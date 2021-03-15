import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='SNR',
    version='0.6.1',
    author='Spencer Shaw',
    author_email='calpolyroboticsclub@gmail.com',
    packages=find_packages(where='.',
                           exclude=['tests']),  # type: ignore
    url='http://github.com/sfshaw-calpoly/SNR',
    license='LICENSE.txt',
    description='Soft-realtime robotics framework for education',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'typing_extensions;python_version<"3.8"',   # Protocol backport
        'dataclasses;python_version<"3.7"',         # Dataclasses backport
        'dataclasses_json>=0.5.2',                  # Serialization
        # 'numpy>=1.20.0',                            # Kalman filter, CV
        # 'pygame>=2.0.0'                             # Controller
        'pyserial>=3.5',                            # Serial connection
        # 'pysimplegui=4.29.0',                       # GUI
    ],
    extras_require={
        'dev': [
            'pip>=21.0',
            'setuptools',
            'wheel',
            'pdoc>=6.1',        # Doc generation
            'nox',              # Test automation, venv
            'pytest',           # Type checking
            'pytest-timeout',   # Test timeout
            'mypy>=0.800',      # Type checking
            'flake8>=3.8',      # Linter
        ],
    },
    python_requires='>=3.6'
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'Topic :: Education',
        'Topic :: Robotics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Operating System :: POSIX :: Linux',

        'Typing :: Typed',
    ],
)
