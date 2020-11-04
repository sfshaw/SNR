CPYTHON=python3.9
PYPY=pypy3
PYTHON=$(CPYTHON)

SETUP_PY=setup.py
PY_SETUP=$(PYTHON) $(SETUP_PY)

BUILD_DIR=build
DIST_DIR=dist
SRC_DIR=snr
TEST_DIR=$(SRC_DIR)/test

TEST1=test1.py

TEST_FLAGS=test -d
FILE_UNDER_TEST=$(TEST1)

.PHNOY: dev check build install dist test
dev:
	$(PY_SETUP) develop --user

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

clean:
	$(PY_SETUP) clean
	rm -rf ./$(BUILD_DIR) ./$(DIST_DIR)

py:
	$(PYTHON)
