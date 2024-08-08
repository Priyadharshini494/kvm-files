import ctypes
import ctypes.util

from ctypes import c_int
from ctypes import c_uint
from ctypes import c_uint32
from ctypes import c_char_p
from ctypes import c_void_p


# =====
def _load_libc() -> ctypes.CDLL:
    path = ctypes.util.find_library("c")
    if not path:
        raise RuntimeError("Where is libc?")
    assert path
    lib = ctypes.CDLL(path)
    for (name, restype, argtypes) in [
        ("inotify_init", c_int, []),
        ("inotify_add_watch", c_int, [c_int, c_char_p, c_uint32]),
        ("inotify_rm_watch", c_int, [c_int, c_uint32]),
        ("renameat2", c_int, [c_int, c_char_p, c_int, c_char_p, c_uint]),
        ("free", c_int, [c_void_p]),
    ]:
        func = getattr(lib, name)
        if not func:
            raise RuntimeError(f"Where is libc.{name}?")
        setattr(func, "restype", restype)
        setattr(func, "argtypes", argtypes)
    return lib


_libc = _load_libc()


# =====
get_errno = ctypes.get_errno

inotify_init = _libc.inotify_init
inotify_add_watch = _libc.inotify_add_watch
inotify_rm_watch = _libc.inotify_rm_watch
renameat2 = _libc.renameat2
free = _libc.free
