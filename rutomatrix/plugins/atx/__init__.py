from typing import AsyncGenerator

from ...errors import OperationError
from ...errors import IsBusyError

from .. import BasePlugin
from .. import get_plugin_class


# =====
class AtxError(Exception):
    pass


class AtxOperationError(OperationError, AtxError):
    pass


class AtxIsBusyError(IsBusyError, AtxError):
    def __init__(self) -> None:
        super().__init__("Performing another ATX operation, please try again later")


# =====
class BaseAtx(BasePlugin):
    async def get_state(self) -> dict:
        raise NotImplementedError

    async def poll_state(self) -> AsyncGenerator[dict, None]:
        yield {}
        raise NotImplementedError

    async def cleanup(self) -> None:
        pass

    # =====

    async def power_on(self, wait: bool) -> None:
        raise NotImplementedError

    async def power_off(self, wait: bool) -> None:
        raise NotImplementedError

    async def power_off_hard(self, wait: bool) -> None:
        raise NotImplementedError

    async def power_reset_hard(self, wait: bool) -> None:
        raise NotImplementedError

    # =====

    async def click_power(self, wait: bool) -> None:
        raise NotImplementedError

    async def click_power_long(self, wait: bool) -> None:
        raise NotImplementedError

    async def click_reset(self, wait: bool) -> None:
        raise NotImplementedError


# =====
def get_atx_class(name: str) -> type[BaseAtx]:
    return get_plugin_class("atx", name)  # type: ignore
