CPYTHON=python3

CPYTHON36=python3.6
CPYTHON37=python3.7
CPYTHON38=python3.8
CPYTHON39=python3.9
CPYTHON310=python3.10
PYPY=pypy3

PYTHON=$(CPYTHON)

SETUP_PY=setup.py
PY_SETUP=$(PYTHON) $(SETUP_PY)
UNITTEST_MOD=-m unittest

BUILD_DIR=build
DIST_DIR=dist
EGG_INFO_DIR=SNR.egg-info
LIB_DIR=snr
STD_DIR=snr_std

TEST_FLAGS=test -d

FLAKE8_IGNORE_CODES=F401,F403,F405,W503,W504
FLAKE8_FLAGS=snr --ignore=$(FLAKE8_IGNORE_CODES)

.PHONY: dev develop console check build install dist test test_all clean pygame_deps lint flake mypy prep
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

dist: build
	$(PY_SETUP) sdist

install: build
	$(PY_SETUP) install --user

t: test
test: check
	$(PYTHON) $(UNITTEST_MOD)

ta: test_all
test_all:
	$(CPYTHON36) $(UNITTEST_MOD)
	$(CPYTHON37) $(UNITTEST_MOD)
	$(CPYTHON38) $(UNITTEST_MOD)
	$(CPYTHON39) $(UNITTEST_MOD)
	$(CPYTHON310) $(UNITTEST_MOD)
	$(PYPY) $(UNITTEST_MOD)

prep: test_all lint

l: lint
lint: mypy flake

f: flake
flake: 
	flake8 $(FLAKE8_FLAGS)

my: mypy
mypy:
	mypy $(LIB_DIR)

c: clean
clean:
	$(PY_SETUP) clean
	py3clean .
	rm -rf ./$(BUILD_DIR) ./$(DIST_DIR) ./$(EGG_INFO_DIR)

py:
	$(PYTHON)

pygame_deps: 
	sudo apt update
	sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev
	sudo apt-get build-dep libsdl2 libsdl2-image libsdl2-mixer libsdl2-ttf libfreetype6 libportmidi0
