from snr.core.base import *
from snr.types import *

from . import console

Command = Callable[[List[str]], SomeTasks]


class CommandProcessor(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "command_processor")
        self.task_handlers = {
            (TaskType.store_page, console.COMMAND_DATA_NAME):
            self.process_command}
        self.commands: Dict[str, Command] = {
            "exit": self.cmd_exit,
            "task": self.cmd_schedule_task,
            "reload": self.cmd_reload,
            "list": self.cmd_list,
        }
        self.log.setLevel(logging.WARNING)

    def task_source(self) -> None:
        return None

    def process_command(self, task: Task, key: TaskId) -> SomeTasks:
        command_page: Page = task.val_list[0]
        assert command_page is not None
        args: List[str] = command_page.data
        self.dbg("Processing command: %s", args)
        if args:
            command = self.commands.get(args[0])
            if command:
                result: SomeTasks = command(args[1:])
                return result
        return None

    def cmd_schedule_task(self, args: List[str]) -> Task:
        type = TaskType(args[0])
        return Task(type, args[1], val_list=args[1:])

    def cmd_exit(self, args: List[str]) -> Task:
        self.dbg("Executing exit command")
        return task_terminate("terminate_cmd")

    def cmd_reload(self, args: List[str]) -> SomeTasks:
        if len(args) == 1:
            return task_reload(args[0])
        else:
            self.warn("Invalid reload args: %s", args)
            return None

    def cmd_list(self, args: List[str]) -> SomeTasks:
        self.info("Listing endpoints: \n%s",
                  "\n\t".join(self.parent.endpoints.keys()))
        return None
