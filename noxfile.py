from typing import List

import nox

supported_python_versions: List[str] = [
    'python3.7',
    'python3.8',
    'python3.9',
    'python3.10',
    'pypy3',
]


@nox.session(python=supported_python_versions,
             reuse_venv=True)
def tests(session: nox.Session):
    # list(map(
    session.install('.[test]')
    session.run('pytest', external=False)


@nox.session(python='3',
             reuse_venv=True)
def mypy(session: nox.Session):
    session.install('.[mypy]')
    session.run('mypy', '-p', 'snr')

@nox.session(python='3',
             reuse_venv=True)
def lint(session: nox.Session):
    session.install('.[lint]')
    session.run('flake8', 'snr', 'tests')
