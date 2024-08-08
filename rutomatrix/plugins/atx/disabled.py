from typing import AsyncGenerator

from ... import aiotools

from . import AtxOperationError
from . import BaseAtx


# =====
class AtxDisabledError(AtxOperationError):
    def __init__(self) -> None:
        super().__init__("ATX is disabled")


# =====
class Plugin(BaseAtx):
    async def get_state(self) -> dict:
        return {
            "enabled": False,
            "busy": False,
            "leds": {
                "power": False,
                "hdd": False,
            },
        }

    async def poll_state(self) -> AsyncGenerator[dict, None]:
        while True:
            yield (await self.get_state())
            await aiotools.wait_infinite()

    # =====

    async def __stub(self, wait: bool) -> None:
        raise AtxDisabledError()

    power_on = power_off = power_off_hard = power_reset_hard = __stub
    click_power = click_power_long = click_reset = __stub
