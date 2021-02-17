import nox
import project_requires


@nox.session(python=project_requires.supported_python_versions,
             reuse_venv=True)
def tests(session: nox.Session):
    # list(map(
    session.install(*project_requires.install_deps)
    list(map(session.install, project_requires.test_deps))
    session.run('pytest', external=False)


@nox.session(python='3',
             reuse_venv=True)
def mypy(session: nox.Session):
    list(map(session.install, project_requires.lint_deps))
    session.run('mypy', '-p', 'snr')


@nox.session(python='3',
             reuse_venv=True)
def lint(session: nox.Session):
    list(map(session.install, project_requires.lint_deps))
    session.run('flake8', 'snr', 'tests')
