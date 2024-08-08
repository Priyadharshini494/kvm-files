import asyncio

from typing import Any

import async_lru

from aiohttp.web import Request
from aiohttp.web import Response

from .... import tools

from ....htserver import exposed_http

from ....plugins.atx import BaseAtx
from ....plugins.ugpio import UserGpioModes

from ..info import InfoManager
from ..ugpio import UserGpio


# =====
class ExportApi:
    def __init__(self, info_manager: InfoManager, atx: BaseAtx, user_gpio: UserGpio) -> None:
        self.__info_manager = info_manager
        self.__atx = atx
        self.__user_gpio = user_gpio

    # =====

    @exposed_http("GET", "/export/prometheus/metrics")
    async def __prometheus_metrics_handler(self, _: Request) -> Response:
        return Response(text=(await self.__get_prometheus_metrics()))

    @async_lru.alru_cache(maxsize=1, ttl=5)
    async def __get_prometheus_metrics(self) -> str:
        (atx_state, hw_state, fan_state, gpio_state) = await asyncio.gather(*[
            self.__atx.get_state(),
            self.__info_manager.get_submanager("hw").get_state(),
            self.__info_manager.get_submanager("fan").get_state(),
            self.__user_gpio.get_state(),
        ])
        rows: list[str] = []

        self.__append_prometheus_rows(rows, atx_state["enabled"], "rutomatrix_atx_enabled")  # type: ignore
        self.__append_prometheus_rows(rows, atx_state["leds"]["power"], "rutomatrix_atx_power")  # type: ignore

        for mode in sorted(UserGpioModes.ALL):
            for (channel, ch_state) in gpio_state[f"{mode}s"].items():  # type: ignore
                if not channel.startswith("__"):  # Hide special GPIOs
                    for key in ["online", "state"]:
                        self.__append_prometheus_rows(rows, ch_state["state"], f"rutomatrix_gpio_{mode}_{key}_{channel}")

        self.__append_prometheus_rows(rows, hw_state["health"], "rutomatrix_hw")  # type: ignore
        self.__append_prometheus_rows(rows, fan_state, "rutomatrix_fan")

        return "\n".join(rows)

    def __append_prometheus_rows(self, rows: list[str], value: Any, path: str) -> None:
        if isinstance(value, bool):
            value = int(value)
        if isinstance(value, (int, float)):
            rows.extend([
                f"# TYPE {path} gauge",
                f"{path} {value}",
                "",
            ])
        elif isinstance(value, dict):
            for (sub_key, sub_value) in tools.sorted_kvs(value):
                sub_path = (f"{path}_{sub_key}" if sub_key != "parsed_flags" else path)
                self.__append_prometheus_rows(rows, sub_value, sub_path)