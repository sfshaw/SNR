import logging
from typing import Callable, Dict, List, Tuple

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *

from . import remote_console

Command = str
HelpText = str
CommandFn = Callable[[List[str]], str]
CommandDict = Dict[Command,
                   Tuple[HelpText,
                         CommandFn]]


class CommandProcessor(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "command_processor")
        self.log.setLevel(logging.INFO)
        self.task_handlers = {
            (TaskType.store_page, remote_console.COMMAND_DATA_NAME):
            self.process_command}
        self.commands: CommandDict = {
            "exit": ("Terminate the node and console",
                     self.cmd_exit),
            "task": ("Schedule a task",
                     self.cmd_schedule_task),
            "reload": ("Reload 'all' or a specific endpoint",
                       self.cmd_reload),
            "list": ("List all 'commands' or 'endpoints'",
                     self.cmd_list),
            "dump": ("Dump data from 'profiler' or 'datastore'",
                     self.cmd_dump),
            "help": ("List all commands",
                     self.cmd_help),
        }

    def task_source(self) -> None:
        return None

    def process_command(self, task: Task, key: TaskId) -> SomeTasks:
        command_page: Page = task.val_list[0]
        assert command_page is not None
        args: List[str] = command_page.data
        self.dbg("Processing command: %s", args)
        response: str = "No command or arguments given"
        if args:
            command = self.commands.get(args[0])
            if command:
                response = command[1](args[1:])
            else:
                response = f"Invalid command {args[0]}"

        return tasks.store_page(self.parent.page(
            remote_console.COMMAND_ACK_DATA_NAME,
            response))

    def cmd_schedule_task(self, args: List[str]) -> str:
        type = TaskType(args[0])
        t = Task(type, args[1], val_list=args[1:])
        self.parent.schedule(t)
        return f"Scheduled {t}"

    def cmd_exit(self, args: List[str]) -> str:
        self.dbg("Executing exit command")
        self.parent.schedule(tasks.terminate("terminate_cmd"))
        return "Terminating"

    def cmd_reload(self, args: List[str]) -> str:
        message = f"Invalid reload args: {args}"
        if len(args) == 1:
            target = args[0]
            if target == "all":
                for component_name in self.parent.components.keys():
                    self.schedule(tasks.reload_component(component_name))
            else:
                self.parent.schedule(tasks.reload_component(target))
            return f"Reloading {target}"
        else:
            self.warn(message)
        return message

    def cmd_help(self, args: List[str]):
        if len(args) > 0:
            cmd = self.commands.get(args[0])
            if cmd:
                return f"Command:\n\t{args[0]}:\t{cmd[0]}"
            else:
                return f"No command {args[0]}"
        return self.cmd_list(["commands"])

    def cmd_list(self, args: List[str]) -> str:
        if len(args) > 0 and args[0] == "endpoints":
            message = "Listing endpoints:\n\t" + \
                "\n\t".join(self.parent.components.keys())
        else:
            lines = [f"{key}:\t{help}"
                     for (key, (help, _)) in self.commands.items()]
            message = "Listing commands:\n\t" + \
                "\n\t".join(lines)
        self.dbg(message)
        return message

    def cmd_dump(self, args: List[str]) -> str:
        if len(args) > 0 and args[0] == "profiler":
            if self.parent.profiler:
                message = self.parent.profiler.dump()
            else:
                message = "No profiling data found"

        elif len(args) > 0 and args[0] == "datastore":
            message = self.parent.dump_data()

        else:
            return self.cmd_help(["dump"])
        self.dbg(message)
        return message

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
