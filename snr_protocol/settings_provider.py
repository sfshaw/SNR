from snr_types import *


@runtime_checkable
class SettingsProvider(Protocol):
    settings: Settings
