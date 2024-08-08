from typing import Callable
from typing import Any

import gpiod

from ... import aiotools
from ... import aiogp

from ...yamlconf import Option

from ...validators.os import valid_abs_path
from ...validators.hw import valid_gpio_pin

from . import BaseUserGpioDriver


# =====
class Plugin(BaseUserGpioDriver):
    def __init__(
        self,
        instance_name: str,
        notifier: aiotools.AioNotifier,

        device_path: str,
    ) -> None:

        super().__init__(instance_name, notifier)

        self.__device_path = device_path

        self.__input_pins: dict[int, aiogp.AioReaderPinParams] = {}
        self.__output_pins: dict[int, (bool | None)] = {}

        self.__reader: (aiogp.AioReader | None) = None

        self.__chip: (gpiod.Chip | None) = None
        self.__output_lines: dict[int, gpiod.Line] = {}

    @classmethod
    def get_plugin_options(cls) -> dict:
        return {
            "device": Option("/dev/gpiochip0", type=valid_abs_path, unpack_as="device_path"),
        }

    @classmethod
    def get_pin_validator(cls) -> Callable[[Any], Any]:
        return valid_gpio_pin

    def register_input(self, pin: str, debounce: float) -> None:
        self.__input_pins[int(pin)] = aiogp.AioReaderPinParams(False, debounce)

    def register_output(self, pin: str, initial: (bool | None)) -> None:
        self.__output_pins[int(pin)] = initial

    def prepare(self) -> None:
        assert self.__reader is None
        self.__reader = aiogp.AioReader(
            path=self.__device_path,
            consumer="rutomatrix::gpio::inputs",
            pins=self.__input_pins,
            notifier=self._notifier,
        )

        self.__chip = gpiod.Chip(self.__device_path)
        for (pin, initial) in self.__output_pins.items():
            line = self.__chip.get_line(pin)
            line.request("rutomatrix::gpio::outputs", gpiod.LINE_REQ_DIR_OUT, default_vals=[int(initial or False)])
            self.__output_lines[pin] = line

    async def run(self) -> None:
        assert self.__reader
        await self.__reader.poll()

    async def cleanup(self) -> None:
        if self.__chip:
            try:
                self.__chip.close()
            except Exception:
                pass

    async def read(self, pin: str) -> bool:
        assert self.__reader
        pin_int = int(pin)
        if pin_int in self.__input_pins:
            return self.__reader.get(pin_int)
        return bool(self.__output_lines[pin_int].get_value())

    async def write(self, pin: str, state: bool) -> None:
        self.__output_lines[int(pin)].set_value(int(state))

    def __str__(self) -> str:
        return f"GPIO({self._instance_name})"

    __repr__ = __str__
