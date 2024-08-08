from aiohttp.web import Request
from aiohttp.web import Response

from ....htserver import exposed_http
from ....htserver import make_json_response

from ....validators.basic import valid_bool
from ....validators.basic import valid_float_f0
from ....validators.ugpio import valid_ugpio_channel

from ..ugpio import UserGpio


# =====
class UserGpioApi:
    def __init__(self, user_gpio: UserGpio) -> None:
        self.__user_gpio = user_gpio

    # =====

    @exposed_http("GET", "/gpio")
    async def __state_handler(self, _: Request) -> Response:
        return make_json_response({
            "model": (await self.__user_gpio.get_model()),
            "state": (await self.__user_gpio.get_state()),
        })

    @exposed_http("POST", "/gpio/switch")
    async def __switch_handler(self, request: Request) -> Response:
        channel = valid_ugpio_channel(request.query.get("channel"))
        state = valid_bool(request.query.get("state"))
        wait = valid_bool(request.query.get("wait", False))
        await self.__user_gpio.switch(channel, state, wait)
        return make_json_response()

    @exposed_http("POST", "/gpio/pulse")
    async def __pulse_handler(self, request: Request) -> Response:
        channel = valid_ugpio_channel(request.query.get("channel"))
        delay = valid_float_f0(request.query.get("delay", 0.0))
        wait = valid_bool(request.query.get("wait", False))
        await self.__user_gpio.pulse(channel, delay, wait)
        return make_json_response()
