from typing import List

supported_python_versions: List[str] = [
    'python3.7',
    'python3.8',
    'python3.9',
    'python3.10',
    'pypy3',
]

install_deps: List[str] = [
    'dataclasses;python_version<"3.7"',         # Dataclasses backport
    'dataclasses_json>=0.5.2',                  # Serialization
    # 'numpy>=1.20.0',                            # Kalman filter, CV
    # 'pygame>=2.0.0'                           # Controller
    'pyserial>=3.5',                            # Serial connection
    # 'pysimplegui=4.29.0',                     # GUI
    'typing;python_version<"3.7"',              # Typing backports
    'typing-extensions;python_version<"3.7"',   # Protocol backport
]

test_deps: List[str] = [
    'pytest',          # Type checking
    'pytest-timeout',          # Linter
]

lint_deps: List[str] = [
    'mypy>=0.800',          # Type checking
    'flake8>=3.8',          # Linter
]

docs_deps: List[str] = ['pdoc>=6.1']

# lint_cmds = [
#     ['mypy', '-p', 'snr'],
#     'flake8',
# ]
