from typing import List

import nox

DEFAULT_PYTHON_VERSION: str = '3'
SUPPORTED_PYTHON_VERSIONS: List[str] = [
    '3.7',
    '3.8',
    '3.9',
    '3.10',
    'pypy-3.7',
]


@nox.session(python=DEFAULT_PYTHON_VERSION,
             reuse_venv=True)
def test(session: nox.Session):
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-test.txt')
    session.run('pytest', external=False)


@nox.session(python=SUPPORTED_PYTHON_VERSIONS,
             reuse_venv=True)
def test_all(session: nox.Session):
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-test.txt')
    session.run('pytest', external=False)


@nox.session(python=DEFAULT_PYTHON_VERSION,
             reuse_venv=True)
def mypy(session: nox.Session):
    session.install('mypy')
    session.run('mypy', '-p', 'snr')


@nox.session(python=DEFAULT_PYTHON_VERSION,
             reuse_venv=True)
def lint(session: nox.Session):
    session.install('flake8')
    session.run('flake8', 'snr', 'tests')
