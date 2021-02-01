from snr.snr_core.base import *

Command = Callable[[List[str]], SomeTasks]


class CommandProcessor(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "console_server")
        self.task_handlers = {
            (TaskType.process_data, "console_cmd"):
            self.process_command}
        self.commands: Dict[str, Command] = {
            "exit": self.cmd_exit,
            "task": self.cmd_schedule_task,
            "reload": self.cmd_reload,
            "list": self.cmd_list,
        }

    def task_source(self) -> None:
        return None

    def process_command(self, cmd_task: Task, key: TaskId) -> SomeTasks:
        args: List[str] = cmd_task.val_list
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
        return task.terminate("terminate_cmd")

    def cmd_reload(self, args: List[str]):
        if len(args) == 1:
            return task.reload(args[1])
        else:
            self.warn("Invalid reload args: %s", args)

    def cmd_list(self, args: List[str]) -> SomeTasks:
        options = {
            "endpoints": task.event("cmd_list_endpoints")
        }
        return options.get(args[0])
