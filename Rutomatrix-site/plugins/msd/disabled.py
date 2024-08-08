import contextlib

from typing import AsyncGenerator

from ... import aiotools

from . import MsdOperationError
from . import BaseMsdReader
from . import BaseMsdWriter
from . import BaseMsd


# =====
class MsdDisabledError(MsdOperationError):
    def __init__(self) -> None:
        super().__init__("MSD is disabled")


# =====
class Plugin(BaseMsd):
    async def get_state(self) -> dict:
        return {
            "enabled": False,
            "online": False,
            "busy": False,
            "storage": None,
            "drive": None,
        }

    async def poll_state(self) -> AsyncGenerator[dict, None]:
        while True:
            yield (await self.get_state())
            await aiotools.wait_infinite()

    async def reset(self) -> None:
        raise MsdDisabledError()

    # =====

    async def set_params(
        self,
        name: (str | None)=None,
        cdrom: (bool | None)=None,
        rw: (bool | None)=None,
    ) -> None:

        raise MsdDisabledError()

    async def set_connected(self, connected: bool) -> None:
        raise MsdDisabledError()

    @contextlib.asynccontextmanager
    async def read_image(self, name: str) -> AsyncGenerator[BaseMsdReader, None]:
        if self is not None:  # XXX: Vulture and pylint hack
            raise MsdDisabledError()
        yield BaseMsdReader()

    @contextlib.asynccontextmanager
    async def write_image(self, name: str, size: int, remove_incomplete: (bool | None)) -> AsyncGenerator[BaseMsdWriter, None]:
        if self is not None:  # XXX: Vulture and pylint hack
            raise MsdDisabledError()
        yield BaseMsdWriter()

    async def remove(self, name: str) -> None:
        raise MsdDisabledError()
