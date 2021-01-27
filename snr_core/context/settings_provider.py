from typing import Protocol
from snr_core.settings import Settings


class SettingsProvider(Protocol):
    settings: Settings
