from snr.config import Config, MODE_DEBUG, MODE_DEPLOYED
import sys

from snr.node import Node
from snr.utils.utils import print_exit, print_usage
from snr.context import root_context


class Runner:

    def __init__(self, config: Config):
        argc = len(sys.argv)
        if argc < 2:
            print_usage()
            sys.exit(1)
        self.role = sys.argv[1]

        self.mode = MODE_DEPLOYED
        if "-d" in sys.argv:
            self.mode = MODE_DEBUG
        
        self.components = config.get(self.mode)[self.role]

    def run(self):
        context = root_context("runner")
        py_v: str = sys.version[0:5]
        context.info("Starting {} node in {} mode using Python {}", [
                     self.role, self.mode, py_v])
        node = None
        try:
            node = Node(context, self.role, self.mode, self.components)
            node.loop()  # Blocking loop
        except KeyboardInterrupt:
            if node:
                context.log("framework", "Interrupted by user, exiting")
                node.set_terminate_flag("Interrupted by user")
            else:
                context.fatal("Exiting before node was done being constructed")
        finally:
            if node:
                node.terminate()
                node = None
        context.terminate()
        print_exit("Ya done now")
