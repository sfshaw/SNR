from snr.core.base import *
from snr.types import *

from . import console

Command = Callable[[List[str]], str]


class CommandProcessor(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "command_processor")
        self.log.setLevel(logging.INFO)
        self.task_handlers = {
            (TaskType.store_page, console.COMMAND_DATA_NAME):
            self.process_command}
        self.commands: Dict[str, Tuple[str, Command]] = {
            "exit": ("Terminate the node and console", self.cmd_exit),
            "task": ("Schedule a task", self.cmd_schedule_task),
            "reload": ("Reload 'all' or a specific endpoint", self.cmd_reload),
            "list": ("List all 'commands' or 'endpoints'", self.cmd_list),
            "help": ("List all commands", self.cmd_help),
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

        return task_store_page(self.parent.make_page(
            console.COMMAND_ACK_DATA_NAME, response))

    def cmd_schedule_task(self, args: List[str]) -> str:
        type = TaskType(args[0])
        t = Task(type, args[1], val_list=args[1:])
        self.parent.schedule(t)
        return f"Scheduled {t}"

    def cmd_exit(self, args: List[str]) -> str:
        self.dbg("Executing exit command")
        self.parent.schedule(task_terminate("terminate_cmd"))
        return "Terminating"

    def cmd_reload(self, args: List[str]) -> str:
        message = f"Invalid reload args: {args}"
        if len(args) == 1:
            target = args[0]
            if target == "all":
                for endpoint_name in self.parent.endpoints.keys():
                    self.parent.schedule(task_reload(endpoint_name))
            else:
                self.parent.schedule(task_reload(target))
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
                "\n\t".join(self.parent.endpoints.keys())
        else:
            lines = [f"{key}:\t{help}"
                     for (key, (help, _)) in self.commands.items()]
            message = "Listing commands:\n\t" + \
                "\n\t".join(lines)
        self.dbg(message)
        return message
