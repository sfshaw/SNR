from snr import *
import pygame


class ControllerLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory, parent,
                         "controller_loop",
                         max_tick_rate_hz=5)

    def setup(self) -> None:
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        print(f"Found joysticks: {joysticks}")

    def loop(self) -> None:
        print("Loop d'loop")

    def halt(self) -> None:
        print("Loop halted")

    def terminate(self) -> None:
        pygame.joystick.quit()
        print("Loop terminated")
