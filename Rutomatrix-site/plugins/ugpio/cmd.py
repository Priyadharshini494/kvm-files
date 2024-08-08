from typing import Callable
from typing import Any

from ...logging import get_logger

from ... import tools
from ... import aiotools
from ... import aioproc

from ...yamlconf import Option

from ...validators.os import valid_command

from . import GpioDriverOfflineError
from . import UserGpioModes
from . import BaseUserGpioDriver


# =====
class Plugin(BaseUserGpioDriver):  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=super-init-not-called
        self,
        instance_name: str,
        notifier: aiotools.AioNotifier,

        cmd: list[str],
    ) -> None:

        super().__init__(instance_name, notifier)

        self.__cmd = cmd

    @classmethod
    def get_plugin_options(cls) -> dict:
        return {
            "cmd": Option([], type=valid_command),
        }

    @classmethod
    def get_modes(cls) -> set[str]:
        return set([UserGpioModes.OUTPUT])

    @classmethod
    def get_pin_validator(cls) -> Callable[[Any], Any]:
        return str

    async def read(self, pin: str) -> bool:
        _ = pin
        return False

    async def write(self, pin: str, state: bool) -> None:
        _ = pin
        if not state:
            return
        try:
            proc = await aioproc.log_process(self.__cmd, logger=get_logger(0), prefix=str(self))
            if proc.returncode != 0:
                raise RuntimeError(f"Custom command error: retcode={proc.returncode}")
        except Exception as err:
            get_logger(0).error("Can't run custom command [ %s ]: %s",
                                tools.cmdfmt(self.__cmd), tools.efmt(err))
            raise GpioDriverOfflineError(self)

    def __str__(self) -> str:
        return f"CMD({self._instance_name})"

    __repr__ = __str__
