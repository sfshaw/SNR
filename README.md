# SNR

[![Python unit Tests](https://github.com/sfshaw-calpoly/SNR/workflows/Python%20unit%20tests/badge.svg)](https://github.com/sfshaw-calpoly/SNR/actions?query=workflow%3A%22Python+unit+tests%22)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

SNR provides a soft-realtime robotics framework for education. It was originally developed for the Cal Poly Robotics Club Underwater Remote Operated Vehicle (UROV). SNR aims to provide a platform for teaching robotics, systems design, and embedded programming. SNR provides paradigms similar to [ROS](https://www.ros.org/) and NASA's [F´](https://github.com/nasa/fprime) but in a simpler stack.

## Get Started
Install SNR from source

    git clone https://github.com/sfshaw-calpoly/SNR
    cd SNR
    python3 -m pip install . --user --upgrade

Typical usage for the CPRC UROV might have a `main.py` like this:

    from snr import *
    
    def main():
        sockets_pair = SocketsPair(...)
        config = Config(Mode.DEPLOYED, {
            'topside': [
                XBoxControllerFactory(),
                InputProcessorFactory(),
                sockets_pair.server_factory,
                ],
            'urov': [
                sockets_pair.client_factory,
                ControlsProcessorFactory(),
                MotorControllerFactory(),
                SerialConnectionFactory(),
                SensorsProcessorFactory(),
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
- Endpoints provide synchronous task handlers to the Node's event loop
- Loops run in their own loop context, separate from the Node's event loop
- Each node has a role, a set of Endpoints and Loops, and a Datastore
- Endpints and Loops can read and write key-value pairs (Pages) to their parent node's Datastore
- Endpoints and Loops can schedule events (Tasks) for their parent node's event loop (TaskQueue)
- Nodes are wrapped in Runners, which construct them based on a Config
- Configs contain a map of roles to component Factories
- Factories construct Endpoints and Loops, enabling hot-reloading

## Architecture and Repo Structure
### Submodules (shown in order of dependance) 
    
    ./snr/snr_types     # Type definitions used throughout the project 
    ./snr/snr_protocol  # Protocol (interface) definitions implemented by core, std, and user code
    ./snr/snr_core      # Concrete implementations of core classes including runners, Node, and other base classes 
    ./snr/snr_std       # Useful ready made components that can be used by user code

### Top level project files
    CHANGES.txt     # Project changelog
    LICENSE.txt     # Project license
    MANIFEST.in     # Python package manifest file
    Makefile        # "A Bash Notebook"
    README.md       # This README file
    bin             # Binary scripts
    mypy.ini        # MyPy configuration
    noxfile.py      # Cross version testing framework configuration
    pyproject.toml  # PEP 518 project configuration 
    python_version  # Lowest supported Python Version
    setup.cfg       # Coverage and Flake8 configuration
    setup.py        # Python package confirugation
    snr             # Root module source directory
    tests           # Automated tests
 
## Contributors

* Spencer Shaw
