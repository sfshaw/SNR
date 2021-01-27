from typing import Protocol

from snr_types import *


class SettingsProvider(Protocol):
    settings: Settings
