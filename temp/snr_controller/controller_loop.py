from typing import Dict, List, Optional
from snr import *
import pygame


class ControllerLoop(ThreadLoop):

    _JOYSTICK_EVENTS: List[int] = [
        pygame.JOYBUTTONUP,
        pygame.JOYBUTTONDOWN,
    ]

    joystick: Optional[pygame.joystick.Joystick]
    num_axes: int
    num_buttons: int

    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 ) -> None:
        super().__init__(factory, parent,
                         "controller_loop",
                         max_tick_rate_hz=5)
        self.joystick = None
        self.num_axes = 0
        self.num_buttons = 0

    def setup(self) -> None:
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        print(f"Found joysticks: {joysticks}")
        self.joystick = joysticks[0]
        self.num_axes = self.joystick.get_numaxes()
        self.num_buttons = self.joystick.get_numbuttons()
        print(f"Using joystick: {self.joystick.get_name()}")

    def loop(self) -> None:
        assert self.joystick is not None
        event = pygame.event.get()
        if event in ControllerLoop._JOYSTICK_EVENTS:
            raw_input: Dict[str, float] = {}
            for axis_id in range(self.num_axes):
                raw_input[f"axis_{axis_id}"] = \
                    self.joystick.get_axis(axis_id)
            for button_id in range(self.num_buttons):
                raw_input[f"button_{button_id}"] = \
                    self.joystick.get_button(button_id)
            self.store_data("raw_controller_input", raw_input)

    def halt(self) -> None:
        print("Loop halted")

    def terminate(self) -> None:
        pygame.joystick.quit()
        print("Loop terminated")
