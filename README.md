# SNR

[![Python unit Tests](https://github.com/sfshaw-calpoly/SNR/workflows/Python%20unit%20tests/badge.svg)](https://github.com/sfshaw-calpoly/SNR/actions?query=workflow%3A%22Python+unit+tests%22)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

SNR provides a python-based robotics framework for education. It was originally developed for the Cal Poly Robotics Club Underwater Remote Operated Vehicle (UROV). SNR aims to provide a platform for teaching robotics, systems design, and embedded programming. SNR provides paradigms similar to [ROS](https://www.ros.org/) and NASA's [F´](https://github.com/nasa/fprime) but in a simpler stack.

## Get Started

Install SNR from source

    git clone https://github.com/sfshaw-calpoly/SNR
    cd SNR
    python3 -m pip install . --user --upgrade

Typical usage for the CPRC UROV might have a `main.py` like this:

    from snr import *
    from urov import *
    
    def main():
        sockets_pair = SocketsPair(...)
        config = Config(Mode.DEPLOYED, {
            'topside': [
                XBoxControllerFactory(...),
                InputProcessorFactory(...),
                sockets_pair.server_factory,
                ],
            'urov': [
                sockets_pair.client_factory,
                ControlsProcessorFactory(),
                MotorControllerFactory(...),
                SerialConnectionFactory(...),
                SensorsProcessorFactory(...),
                ],
        })
        runner = CLIRunner(config)
        runner.run()


    if __name__ == '__main__':
        main()

To run the node on the topside control unit:

    python3 main.py topside   

To run the node on the UROV itself:

    python3 main.py urov

## Paradigms

- User code resides in Endpoints and Loops, encouraging discrete modules of functionality
- Endpoints: provide synchronous task handlers to the Node's event loop
- Loops: run in their own loop context, separate from the Node's event loop
- Each node, identified by a 'role', has a set of Endpoints and Loops, and a datastore (dictionary)
- Endpints and Loops can read and write key-value pairs (Pages) to their parent node's datastore
- Endpoints and Loops can schedule events (Tasks) for their parent node's event loop (TaskQueue)
- Nodes are wrapped in Runners, which construct them based on a Config
- Configs contain a map of roles to component Factories
- Factories construct Endpoints and Loops, enabling hot-reloading

## Architecture and Repo Structure

### Submodules (shown in order of dependance)

    ./snr/type_defs # Type definitions used throughout the project 
    ./snr/protocol  # Protocol (interface) definitions implemented by core, standard, and user code
    ./snr/core      # Concrete implementations of core classes including runners, Node, Endpoint, ThreadLoop, and other base classes 
    ./snr/utils     # Testing utilities
    ./snr/std_mods  # Standard ready made components that can be used by user code

### Top level project files

    CHANGES.txt     # Project changelog
    LICENSE.txt     # Project license
    MANIFEST.in     # Python package manifest file
    Makefile        # "A Bash Notebook" for usefule shell commands
    README.md       # This README file
    bin/            # Executable scripts
    mypy.ini        # MyPy configuration
    noxfile.py      # Cross version testing framework configuration
    pyproject.toml  # PEP 518 project configuration 
    python_version  # Lowest supported Python Version
    setup.cfg       # Coverage and Flake8 configuration
    setup.py        # Python package confirugation
    snr/            # Root module source directory
    tests/          # Automated tests

## Development

    git clone https://github.com/sfshaw-calpoly/SNR
    cd SNR
    python3 -m pip install -e .[dev]
    # break the code
    make test

### Nox

Nox is a tool that makes testing against multiple interpretters very easy. Running Nox will create virtual environments for all available and supported Python interpreters. MyPy and Flake8 are also run in the Nox suite. Github Actions call `nox` when running workflows. The configuration for nox is found in `noxfile.py`.

    nox                  # Run all sessions
    nox -s test          # Run tests with the default python3 interpreter
    nox -s test_all      # Run tests against all available and supported interpreters
    nox -s test_all-3.9  # Run tests against a specific interpreter
    nox -s mypy          # Run MyPy from nox
    nox -s lint          # Run Flake8 from nox

## Style and Environment

Since SNR targets use in education, code should be easy to read and understand. SNR requires versions of python that support improve type annotations and other typing features, including Protocols. Protocol (interface) defintions and type annotations are very important for student learning. Inspecting type annotations is a great way for students to learn what the program is actually doing, rather than just memorizing constructs.

Visual Studio Code provides and environment conducive to investigation of underlying code. SNR code should be compliant with Pylance's (VSCode Python extension) analysis type checking set to strict. MyPy and Flake8 are also use to improve correctness.

## Contributors

- Spencer Shaw
- Your name here
