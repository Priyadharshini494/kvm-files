from typing import Any

from ..keyboard.mappings import KEYMAP

from ..mouse import MouseRange

from . import check_string_in_list

from .basic import valid_number


# =====
def valid_hid_keyboard_output(arg: Any) -> str:
    return check_string_in_list(arg, "Keyboard output", ["usb", "ps2", "disabled"])


def valid_hid_mouse_output(arg: Any) -> str:
    return check_string_in_list(arg, "Mouse output", ["usb", "usb_win98", "usb_rel", "ps2", "disabled"])


def valid_hid_key(arg: Any) -> str:
    return check_string_in_list(arg, "Keyboard key", KEYMAP, lower=False)


def valid_hid_mouse_move(arg: Any) -> int:
    arg = valid_number(arg, name="Mouse move")
    return min(max(MouseRange.MIN, arg), MouseRange.MAX)


def valid_hid_mouse_button(arg: Any) -> str:
    return check_string_in_list(arg, "Mouse button", ["left", "right", "middle", "up", "down"])


def valid_hid_mouse_delta(arg: Any) -> int:
    arg = valid_number(arg, name="Mouse delta")
    return min(max(-127, arg), 127)
