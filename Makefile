CPYTHON=python3
CPYTHON38=python3.8
CPYTHON39=python3.9
PYPY=pypy3
PYTHON=$(CPYTHON39)

SETUP_PY=setup.py
PY_SETUP=$(PYTHON) $(SETUP_PY)

BUILD_DIR=build
DIST_DIR=dist
EGG_INFO_DIR=SNR.egg-info
LIB_DIR=snr
STD_DIR=snr_std

TEST_FLAGS=test -d

.PHONY: dev develop check build install dist test test_all
d: dev
dev: develop
	$(PYTHON) $(LIB_DIR)/dev.py

develop:
	$(PY_SETUP) develop --user

console:
	$(PYTHON) $(STD_DIR)/io/console/console.py

check:
	$(PY_SETUP) check

build: check
	$(PY_SETUP) build

dist: check
	$(PY_SETUP) sdist

install: check
	$(PY_SETUP) install --user

t: test
test: check
	$(PYTHON) -m unittest -v

ta: test_all
test_all: check
	$(CPYTHON38) -m unittest
	$(CPYTHON39) -m unittest

clean:
	$(PY_SETUP) clean
	py3clean .
	rm -rf ./$(BUILD_DIR) ./$(DIST_DIR) ./$(EGG_INFO_DIR)

mypy:
	mypy $(LIB_DIR)

py:
	$(PYTHON)
