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
LIB_DIR=./$(ROOT_MODULE)
BUILD_DIR=./build
DIST_DIR=./dist
EGG_INFO_DIR=SNR.egg-info
HTML_DOCS_DIR=./html
COVERAGE_FILES=.coverage coverage.xml
CLEAN_DIRS=$(BUILD_DIR) $(DIST_DIR) $(EGG_INFO_DIR) $(HTML_DOCS_DIR) $(COVERAGE_FILES) ./temp

.PHONY: dev
d: dev
dev:
	$(PYTHON) $(LIB_DIR)/dev.py

.PHONY: develop
develop:
	$(PY_SETUP) develop --user

.PHONY: console
console:
	$(PYTHON) $(STD_DIR)/io/console/console.py

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

.PHONY: test
t: test
test: check
	$(PYTHON) $(UNITTEST_MOD)

.PHONY: test_all
ta: test_all
test_all:
	$(CPYTHON37) $(UNITTEST_MOD)
	$(CPYTHON38) $(UNITTEST_MOD)
	$(CPYTHON39) $(UNITTEST_MOD)
	$(CPYTHON310) $(UNITTEST_MOD)
	$(PYPY) $(UNITTEST_MOD)

.PHONY: prep
p: prep
prep: lint test_all check

.PHONY: lint
l: lint
lint: mypy flake

.PHONY: flake
f: flake
flake: 
	flake8 $(ROOT_MODULE)

.PHONY: mypy
my: mypy
mypy:
	$(PYTHON) -m mypy -p $(ROOT_MODULE)

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

.PHONY: pygame_deps
pygame_deps: 
	sudo apt update
	sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev
	sudo apt-get build-dep libsdl2 libsdl2-image libsdl2-mixer libsdl2-ttf libfreetype6 libportmidi0
