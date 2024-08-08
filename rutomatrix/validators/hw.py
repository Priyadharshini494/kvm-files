from typing import Any

from . import check_in_list
from . import check_string_in_list
from . import check_re_match
from . import check_len

from .basic import valid_number


# =====
def valid_tty_speed(arg: Any) -> int:
    name = "TTY speed"
    arg = int(valid_number(arg, name=name))
    return check_in_list(arg, name, [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200])


def valid_gpio_pin(arg: Any) -> int:
    return int(valid_number(arg, min=0, name="GPIO pin"))


def valid_gpio_pin_optional(arg: Any) -> int:
    return int(valid_number(arg, min=-1, name="optional GPIO pin"))


def valid_otg_gadget(arg: Any) -> str:
    name = "OTG gadget name"
    return check_len(check_re_match(arg, name, r"^[a-z_][a-z0-9_-]*$"), name, 255)


def valid_otg_id(arg: Any) -> int:
    return int(valid_number(arg, min=0, max=65535, name="OTG ID"))


def valid_otg_ethernet(arg: Any) -> str:
    return check_string_in_list(arg, "OTG Ethernet driver", ["ecm", "eem", "ncm", "rndis", "rndis5"])
