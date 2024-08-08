import operator
import functools
import multiprocessing.queues
import queue
import shlex

from typing import Hashable
from typing import TypeVar


# =====
def remap(value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    return int((value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)


# =====
def cmdfmt(cmd: list[str]) -> str:
    return " ".join(map(shlex.quote, cmd))


def efmt(err: Exception) -> str:
    return f"{type(err).__name__}: {err}"


# =====
def rget(dct: dict, *keys: Hashable) -> dict:
    result = functools.reduce((lambda nxt, key: nxt.get(key, {})), keys, dct)
    if not isinstance(result, dict):
        raise TypeError(f"Not a dict as result: {result!r} from {dct!r} at {list(keys)}")
    return result


_DictKeyT = TypeVar("_DictKeyT")
_DictValueT = TypeVar("_DictValueT")


def sorted_kvs(dct: dict[_DictKeyT, _DictValueT]) -> list[tuple[_DictKeyT, _DictValueT]]:
    return sorted(dct.items(), key=operator.itemgetter(0))


def swapped_kvs(dct: dict[_DictKeyT, _DictValueT]) -> dict[_DictValueT, _DictKeyT]:
    return {value: key for (key, value) in dct.items()}


# =====
def clear_queue(q: multiprocessing.queues.Queue) -> None:  # pylint: disable=invalid-name
    for _ in range(q.qsize()):
        try:
            q.get_nowait()
        except queue.Empty:
            break


# =====
def build_cmd(cmd: list[str], cmd_remove: list[str], cmd_append: list[str]) -> list[str]:
    assert len(cmd) >= 1, cmd
    return [
        cmd[0],  # Executable
        *filter((lambda item: item not in cmd_remove), cmd[1:]),
        *cmd_append,
    ]
