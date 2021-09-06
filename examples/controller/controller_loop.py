from typing import Dict, List, Optional

import pygame
from snr import *


class ControllerLoop(ThreadLoop):

    _JOYSTICK_EVENTS: List[int] = [
        pygame.JOYAXISMOTION,
        pygame.JOYBALLMOTION,
        pygame.JOYHATMOTION,
        pygame.JOYBUTTONUP,
        pygame.JOYBUTTONDOWN,
    ]

    output_data: DataKey
    joystick: Optional[pygame.joystick.Joystick]
    num_axes: int
    num_buttons: int
    num_hats: int

    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 output_data: DataKey,
                 ) -> None:
        super().__init__(factory, parent,
                         "controller_loop",
                         max_tick_rate_hz=20)
        self.output_data = output_data
        pygame.init()
        pygame.display.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        if len(joysticks) < 1:
            self.fatal("Controller not found")
            raise Exception("Controller not found")
        print(f"Found joysticks: {joysticks}")
        self.joystick = joysticks[0]
        self.num_axes = 0
        self.num_buttons = 0
        self.num_hats = 0
        self.joystick.init()

    def setup(self) -> None:
        assert self.joystick is not None
        self.num_axes = self.joystick.get_numaxes()
        self.num_buttons = self.joystick.get_numbuttons()
        self.num_hats = self.joystick.get_numhats()
        print(f"Using joystick: {self.joystick.get_name()}",
              f"with {self.num_axes} axes",
              f"and {self.num_buttons} buttons",
              f"and {self.num_hats} d pads")

    def loop(self) -> None:
        assert self.joystick is not None
        events: List[pygame.event.Event] = pygame.event.get()
        if pygame.QUIT in [e.type for e in events]:
            self.set_terminate_flag()
            return
        if any(event.type in ControllerLoop._JOYSTICK_EVENTS
               for event in events):
            raw_input: Dict[str, float] = {}
            for axis_id in range(self.num_axes):
                raw_input[f"axis_{axis_id}"] = \
                    self.joystick.get_axis(axis_id)
            for button_id in range(self.num_buttons):
                raw_input[f"button_{button_id}"] = \
                    self.joystick.get_button(button_id)
            for hat_id in range(self.num_hats):
                raw_input[f"dhat_{hat_id}"] = \
                    self.joystick.get_hat(hat_id)
            # print(raw_input)
            self.store_data(self.output_data, raw_input)
        else:
            pass

    def halt(self) -> None:
        pygame.joystick.quit()
        pygame.quit()
        print("Loop halted")

    def terminate(self) -> None:
        print("Loop terminated")
