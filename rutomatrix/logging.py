import sys
import types
import logging


# =====
def get_logger(depth: int=1) -> logging.Logger:
    frame: (types.FrameType | None) = sys._getframe(1)  # pylint: disable=protected-access
    assert frame
    frames = []
    while frame:
        frames.append(frame)
        frame = frame.f_back
        if len(frames) - 1 >= depth:
            break
    name = frames[depth].f_globals["__name__"]
    return logging.getLogger(name)
