CPYTHON=python3

CPYTHON37=python3.7
CPYTHON38=python3.8
CPYTHON39=python3.9
CPYTHON310=python3.10
PYPY=pypy3

PYTHON=$(CPYTHON)

SETUP_PY=setup.py
PY_SETUP=$(PYTHON) $(SETUP_PY)
UNITTEST_MOD=-m unittest
DIST_TARGETS=sdist bdist_wheel

ROOT_MODULE=snr
BIN_DIR=./bin
LIB_DIR=./$(ROOT_MODULE)
BUILD_DIR=./build
DIST_DIR=./dist
EGG_INFO_DIR=SNR.egg-info
HTML_DOCS_DIR=./html
COVERAGE_FILES=.coverage coverage.xml
NOX_DIR=.nox
PYTEST_CACHE=.pytest_cache
MYPY_CACHE=.mypy_cache
CLEAN_DIRS=$(BUILD_DIR) $(DIST_DIR) $(EGG_INFO_DIR) $(HTML_DOCS_DIR) $(COVERAGE_FILES) ./temp $(NOX_DIR) $(PYTEST_CACHE) $(MYPY_CACHE)

.PHONY: dev
d: dev
dev:
	$(PYTHON) $(BIN_DIR)/dev

.PHONY: develop
develop:
	$(PY_SETUP) develop --user

.PHONY: console
console:
	$(PYTHON) $(BIN_DIR)/console

check_manifest:
	$(PYTHON) -m check_manifest

.PHONY: check
check:
	$(PY_SETUP) check

.PHONY: build
build: check
	$(PY_SETUP) build

.PHONY: dist
dist: build
	$(PY_SETUP) $(DIST_TARGETS)

.PHONY: install
install: build
	$(PY_SETUP) install --user

.PHONY: nox
n: nox
nox:
	nox

.PHONY: test
t: test
test: 
	$(PYTHON) -m pytest

.PHONY: unittest
ut: unittest
unittest: 
	$(PYTHON) -m unittest

.PHONY: test_all
ta: test_all
test_all:
	nox -s test_all

.PHONY: lint
l: lint
lint: mypy 
	nox -s lint

.PHONY: mypy
my: mypy
mypy:
	nox -s mypy

.PHONY: diagram
diagram: protocols.png
protocols.png: protocols.dot
	dot -Tpng $< -o $@

.PHONY: dot
dot: snr.protocol.loop_protocol.LoopProtocol.dot
snr.protocol.loop_protocol.LoopProtocol.dot:
	pyreverse -o dot -s 0 -c snr.protocol.loop_protocol.LoopProtocol -mn snr 

.PHONY: coverage
cov: coverage
coverage: coverage.xml
	coverage report

coverage.xml: .coverage
	coverage xml

.coverage:
	coverage run -m unittest 

docs: html
html: lint
	$(PYTHON) -m pdoc -o $(HTML_DOCS_DIR) $(ROOT_MODULE)

.PHONY: docs_http
dh: docs_http
docs_http:
	$(PYTHON) -m pdoc $(ROOT_MODULE)

.PHONY: clean
c: clean
clean:
	$(PY_SETUP) clean
	py3clean .
	rm -rf $(CLEAN_DIRS)

py:
	$(PYTHON)

.PHONY: deps
deps:
	$(PYTHON)
	$(PYTHON) -m pip install .[dev] --user

.PHONY: pygame_deps
pygame_deps: 
	sudo apt update
	sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev
	sudo apt-get build-dep libsdl2 libsdl2-image libsdl2-mixer libsdl2-ttf libfreetype6 libportmidi0
