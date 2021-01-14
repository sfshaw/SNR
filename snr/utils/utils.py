"""Various helper utilities used throughout the code
Attempts to document propper usage of such functions
"""

import sys
from typing import Any, Callable, Dict, List, Optional, Union


def print_usage() -> None:
    """Prints a Unix style uasge message on how to start the program
    """
    print(f"usage: {sys.executable} main.py [robot | topside]")


def no_op(*args: Any) -> None:
    pass


def get_all(*args: Any) -> List[Any]:
    factories = args[0]
    all = []
    for f in factories:
        got: Union[List[Any], Any] = f.get(*args[1:])
        if isinstance(got, List):
            all.extend(got)
        else:
            all.append(got)
    return all


def format_message(context_name: str,
                   level: str,
                   message: str,
                   format_args: Optional[List[str]] = None,
                   end: str = "\n"):
    if format_args:
        message = message.format(*format_args)
    return "[{}:\t{}]\t{}{}".format(context_name,
                                    level,
                                    message,
                                    end)


def init_dict(keys: List[str], val: Any) -> Dict[str, Any]:
    d = {}
    for k in keys:
        d[k] = val
    return d


def attempt(action: Callable[[], bool],
            tries: int,
            fail_once: Callable[[Exception], None],
            failure: Callable[[Exception], None]
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
                # raise Exception()

        def fail_once() -> None:
            debug("action", "action failed, retrying")
            sleep(settings.ACTION_RETRY_WAIT)

        def failure(e: Exception) -> None:
            if settings.REQUIRE_ACTION:
                exit("Could not do required action")
            else:
                debug("action", "Ignoring failing action after {} tries",
                      [tries])
                settings.USE_ACTION = False

        attempt(try_action, settings.ACTION_ATTEMPTS, fail_once, failure)
    """
    def try_action() -> Union[Any, Exception]:
        try:
            result = action()
            if not result:
                raise Exception("Attempt failed")
            return result
        except Exception as e:
            return e

    attempts = 1
    result = try_action()
    while (isinstance(result, Exception)):
        if attempts >= tries:
            failure(result)
            return
        fail_once(result)
        result = try_action()
        attempts += 1
