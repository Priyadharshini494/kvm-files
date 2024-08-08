import os
import stat

from typing import Any

from . import raise_error

from .basic import valid_number
from .basic import valid_string_list
from .basic import valid_stripped_string_not_empty


# =====
def valid_abs_path(arg: Any, type: str="", name: str="") -> str:  # pylint: disable=redefined-builtin
    if type:
        if not name:
            name = f"absolute path to existent {type}"
        type = {
            "file": "reg",
            "dir": "dir",
            "link": "lnk",
            "sock": "sock",
            "fifo": "fifo",
            "char": "chr",
            "block": "blk",
        }[type]
    else:
        if not name:
            name = "absolute path"

    arg = os.path.abspath(valid_stripped_string_not_empty(arg, name))

    if type:
        try:
            st = os.stat(arg)
        except Exception as err:
            raise_error(arg, f"{name}: {err}")
        else:
            if not getattr(stat, f"S_IS{type.upper()}")(st.st_mode):
                raise_error(arg, name)

    return arg


def valid_abs_file(arg: Any, name: str="") -> str:
    return valid_abs_path(arg, type="file", name=name)


def valid_abs_dir(arg: Any, name: str="") -> str:
    return valid_abs_path(arg, type="dir", name=name)


def valid_printable_filename(arg: Any, name: str="") -> str:
    if not name:
        name = "printable filename"

    arg = valid_stripped_string_not_empty(arg, name)

    if (
        "/" in arg
        or "\0" in arg
        or arg.startswith(".")
        or arg == "lost+found"
    ):
        raise_error(arg, name)

    arg = "".join(
        (ch if ch.isprintable() else "_")
        for ch in arg[:255]
    )
    return arg


# =====
def valid_unix_mode(arg: Any) -> int:
    return int(valid_number(arg, min=0, name="UNIX mode"))


def valid_options(arg: Any, name: str="") -> list[str]:
    if not name:
        name = "options"
    return valid_string_list(arg, delim=r"[,\t]+", name=name)


def valid_command(arg: Any) -> list[str]:
    cmd = valid_options(arg, name="command")
    if len(cmd) == 0:
        raise_error(arg, "command")
    cmd[0] = valid_abs_file(cmd[0], name="command entry point")
    return cmd
