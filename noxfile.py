from typing import List

import nox

DEFAULT_PYTHON_VERSION: str = '3'
SUPPORTED_PYTHON_VERSIONS: List[str] = [
    '3.6',
    '3.7',
    '3.8',
    '3.9',
    '3.10',
    'pypy3',
    'pypy-3.6',
    'pypy-3.7',
]


nox.options.reuse_existing_virtualenvs = True  # type: ignore


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def test(session: nox.Session):
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-test.txt')
    session.run('pytest',
                '--no-header',
                './tests/',
                external=False)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session: nox.Session):
    session.install('mypy')
    session.run('mypy', '-p', 'snr', '-p', 'tests')


@nox.session(python=DEFAULT_PYTHON_VERSION)
def pytype(session: nox.Session):
    session.install('pytype')
    session.install('-r', 'requirements.txt')
    session.run('pytype', './snr', '-d', 'not-supported-yet')


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session: nox.Session):
    session.install('flake8')
    session.run('flake8', 'snr', 'tests')


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def bench(session: nox.Session):
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-test.txt')
    session.run('python', '-m', 'unittest',
                '-q',
                'tests.bench.bench_node_startup',
                'tests.bench.bench_stress',
                external=False)
