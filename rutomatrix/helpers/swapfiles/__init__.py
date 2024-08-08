import sys
import os

from ... import libc


# =====
def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(f"Usage: {sys.argv[0]} <file1> <file2>")

    result = libc.renameat2(
        -100,  # AT_FDCWD
        os.fsencode(sys.argv[1]),
        -100,
        os.fsencode(sys.argv[2]),
        (1 << 1),  # RENAME_EXCHANGE
    )

    if result != 0:
        raise SystemExit(f"{sys.argv[0]}: {os.strerror(libc.get_errno())}")
