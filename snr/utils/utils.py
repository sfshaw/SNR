"""Various helper utilities used throughout the code
Attempts to document propper usage of such functions
"""

import sys
from typing import Any, Callable, Dict, List, Optional


def print_usage() -> None:
    """Prints a Unix style uasge message on how to start the program
    """
    print(f"usage: {sys.executable} main.py [robot | topside]")


def print_exit(reason: str) -> None:
    """Kills the program after printing the supplied str reason
    """
    sys.stdout.flush()
    sys.stderr.flush()
    print("\nExiting: " + reason.__repr__())
    sys.exit(0)


def no_op(*args: Any) -> None:
    pass


def get_all(*args: Any):
    factories = args[0]
    all = []
    for f in factories:
        all.extend(f.get(*args[1:]))
    return all


def format_message(context_name: str,
                   level: str,
                   message: str,
                   format_args: Optional[List[str]] = None):
    if format_args:
        message = message.format(*format_args)
    return "[{}:\t{}]\t{}\n".format(context_name, level, message)


def init_dict(keys: List[str], val: Any) -> Dict[str, Any]:
    d = {}
    for k in keys:
        d[k] = val
    return d


def attempt(action: Callable[[], bool],
            tries: int,
            fail_once: Callable[[], None],
            failure: Callable[[int], None]
            ) -> None:
    """Wrapper for trying to complete and action with a number of tries
    Should follow this prototype:
    def attempt_action():
        def try_action() -> bool:
            try:
                return True
            except Exception as error:
                debug("channel", "error: {}", [error.__repr__()])
                return False

        def fail_once() -> None:
            debug("action", "action failed, retrying")
            sleep(settings.ACTION_RETRY_WAIT)

        def failure(tries: int) -> None:
            if settings.REQUIRE_ACTION:
                exit("Could not do required action")
            else:
                debug("action", "Ignoring failing action after {} tries",
                      [tries])
                settings.USE_ACTION = False

        attempt(try_action, settings.ACTION_ATTEMPTS, fail_once, failure)
        debug("action", "Did action")
    """
    attempts = 1
    while (not action()):
        if attempts >= tries:
            failure(attempts)
            return
        fail_once()
        attempts += 1
