# SNR

[![Python unit Tests](https://github.com/sfshaw-calpoly/SNR/workflows/Python%20unit%20tests/badge.svg)](https://github.com/sfshaw-calpoly/SNR/actions?query=workflow%3A%22Python+unit+tests%22)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

SNR is a python-based robotics framework for education. It was originally developed for the [Cal Poly Robotics Club](https://www.calpolyrobotics.com/) (CPRC) Underwater Remote Operated Vehicle (UROV). SNR aims to provide a platform for teaching robotics, systems design, and embedded programming. SNR provides paradigms similar to [ROS](https://www.ros.org/) and NASA's [F´](https://github.com/nasa/fprime), but in a simpler stack to avoid compounding learning curves. SNR uses type annotations and type checking to improve the user's awareness of data types in Python.

## Features

- Task handling event loop in main thread
- Additional loops in child threads
- Thread-safe message passing via task events and data storage
- Ability to reload \[Python] modules within the main event loop

## Get Started

### Install

Install SNR from source and dependancies from PyPi

    git clone https://github.com/sfshaw-calpoly/SNR
    cd SNR
    python3 -m pip install . --user --upgrade

### Typical usage

Typical usage for the CPRC UROV project might have a `main.py` like this:

    from snr import *
    from urov import *
    
    # Define a configuration
    sockets_pair = SocketsPair(...)
    config = Config(factories={
        # Define factories for the 'topside' role 
        'topside': [                      
            XBoxControllerFactory(...),
            InputProcessorFactory(...),
            sockets_pair.server_factory,
            ],
        # Define factories for the 'urov' role
        'urov': [
            sockets_pair.client_factory,
            ControlsProcessorFactory(),
            MotorControllerFactory(...),
            SerialConnectionFactory(...),
            SensorsProcessorFactory(...),
            ],
    })
        

    if __name__ == '__main__':
        # Run the configuration based on command line inputs
        CLIRunner(config).run()

#### Run from a shell

To run the node on the topside control unit:

    python3 main.py topside   

To run the node on the UROV itself:

    python3 main.py urov

More examples can be found in [Examples](#Examples) and in the `tests` module

## Architecture and Repo Structure

### Paradigms

- User code resides in Endpoints and Loops, encouraging discrete modules of functionality
- Endpoints: provide synchronous task handlers to the Node's event loop
- Loops: run in their own loop context, separate from the Node's event loop
- Each node, identified by a 'role', has a set of Endpoints and Loops, and a datastore (dictionary)
- Endpints and Loops can read and write key-value pairs (Pages) to their parent node's datastore
- Endpoints and Loops can schedule events (Tasks) for their parent node's event loop (TaskQueue)
- Nodes are wrapped in Runners, which construct them based on a Config
- Configs contain a map of roles to component Factories
- Factories construct Endpoints and Loops, enabling hot-reloading

### Submodules (shown in order of dependance)

    ./snr/type_defs     # Type definitions used throughout the project 
    ./snr/interfaces      # Protocol (interface) definitions implemented by core, standard, and user code
    ./snr/core          # Concrete implementations of core classes including runners, Node, Endpoint, ThreadLoop, and other base classes 
    ./snr/std_mods      # Standard ready made components that can be used by user code
    ./snr/utils         # Testing utilities
    ./tests             # Unit tests of core and standard implementations

## Examples

The `std_mods` module cantains numerous examples of Endpoint, Loop, and Factory implementations. Introductory usage of basic components will be detailed here. Note that these examples might not be kept up to date or correct. This exemplifies the difference between documentation and code. Code is executable and can be check for correctness automatically. The `tests` module is executed by Github Actions on every push. Passing tests are more likely to show working code than documentation is.

These component modules provide an interface from SNR's event loops and user code (in this case, the made up class `MyPersistentState`). `my_endpoint.py` defines an Endpoint that stores a new piece of data whenever it handles a task.

    from snr.core import *
    from . import MyPersistentState

    class MyEndpointEndpoint(Endpoint):
        def __init__(self,
                    factory: EndpointFactory,
                    parent: NodeProtocol,
                    name: str,
                    some_persistent_state: MyPersistentState
                    ...,
                    ) -> None:
            super().__init__(factory, parent, name)
            self.task_handlers = {
                (TaskType.store_page, "relevant_data_key"): self.process_data,
            }
            self.state = some_persistent_state

        def process_data(self, task: Task, key: TaskId) -> SomeTasks:
            result_data = task.val_list[0] + 1
            return self.task_store_data("output_data_key",
                                            result_data)

`my_loop.py` defines a Loop that runs in its own thread. Synchronous task handlers can also be defined here, but they are run in the main event loop thread.

    from snr.core import *
    from . import MyPersistentState


    class MyLoop(ThreadLoop):
        def __init__(self,
                    factory: LoopFactory,
                    parent: NodeProtocol,
                    name: str,
                    data_keys: List[DataKey],
                    some_persistent_state: MyPersistentState
                    ) -> None:
            super().__init__(factory, parent, name)
            self.log.setLevel(logging.WARNING)
            self.state = some_persistent_state
            for key in data_keys:
                self.task_handlers[(TaskType.process_data,
                                    key)
                                ] = self.process_data

        def process_data(self, task: Task, key: TaskId):
            page = self.parent.get_page(task.name)
            if page:
                self.state.do_something(page.key, page.data)

        def setup(self) -> None:
            self.state.open()

        def loop(self) -> None:
            new_data = self.state.check()

        def halt(self) -> None:
            pass

        def terminate(self) -> None:
            self.state.close()

Factory classes are used to construct and reload Endpoints and Loops. Every Endpoint or Loop implementation is accompanied by a factory implementation.

    from typing import Optional
    from . import my_endpoint, my_loop


    class MyEndpointFactory(EndpointFactory):
        def __init__(self):
            super().__init__(my_endpoint)
            self.state: Optional[MyPersisentState]

        def get(self, parent: AbstractNode) -> AbstractEndpoint:
            if not self.state:
                self.state = MyPersistentState()
            return my_endpoint.MyEndpoint(self,
                                          parent,
                                          "my_endpoint_instance",
                                          self.data_keys,
                                          self.state)


    class MyLoopFactory(LoopFactory):
        def __init__(self, data_keys: List[DataKey]):
            super().__init__(my_endpoint)
            self.data_keys = data_keys
            self.state: Optional[MyPersisentState]

        def get(self, parent: AbstractNode) -> AbstractLoop:
            if not self.state:
                self.state = MyPersistentState()
            return my_loop.MyLoop(self,
                                  parent,
                                  "my_loop_instance",
                                  self.state)

## Development

    git clone https://github.com/sfshaw-calpoly/SNR
    cd SNR
    python3 -m pip install -e .[dev]
    # break the code
    nox
    # submit a pull request

### Top level project files

    CHANGES.txt             # Project changelog, disused
    LICENSE.txt             # Project license
    MANIFEST.in             # Python package manifest file
    Makefile                # "A Bash Notebook" for usefule shell commands
    bin/                    # Executable scripts
    mypy.ini                # MyPy configuration
    noxfile.py              # Cross version testing framework configuration
    pyproject.toml          # PEP 518 project configuration 
    python_version          # Lowest supported Python Version
    README.md               # This README file
    requirements-test.txt   # pip install requirements for testing
    requirements.txt        # pip install requirements for testing
    setup.cfg               # Coverage and Flake8 configuration
    setup.py                # Python package confirugation
    snr/                    # Root module source directory
    tests/                  # Python module containing unit tests

### Style and Environment

Since SNR targets use in education, code should be easy to read and understand. AbstractBaseClasses, Protocol defintions, and type annotations are very important for student learning. Inspecting type annotations is a great way for students to learn what the program is actually doing, rather than just memorizing constructs.

Visual Studio Code provides and environment conducive to investigation of underlying code. SNR code should be compliant with Pylance's (VSCode Python extension) analysis type checking set to strict. MyPy and Flake8 are also used to improve correctness.

#### Formatting

- AutoPEP8 should be sufficient for formatting source code.
- If a list, method signautre, or method call does not fit on one line, put all items, parameters, return types, and arguments on individual lines.
- Follow final list items including parameters with a comma to make diffs adding additional items cleaner.

### Nox

Nox is a tool that makes testing against multiple interpretters very easy. Running Nox will create virtual environments for all available and supported Python interpreters. MyPy and Flake8 are also run in the Nox suite. Github Actions call `nox` when running workflows. The configuration for nox is found in `noxfile.py`.

    nox              # Run all sessions
    nox -s test      # Run tests against all available and supported interpreters
    nox -s test-3.9  # Run tests against a specific supported interpreter
    nox -s mypy      # Run MyPy from nox
    nox -s lint      # Run Flake8 from nox

## Contributors

- Spencer Shaw
- Your name or cheesy pseudonym here
