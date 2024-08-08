from . import tools


# =====
class MouseRange:
    MIN = -32768
    MAX = 32767
    RANGE = (MIN, MAX)

    @classmethod
    def remap(cls, value: int, out_min: int, out_max: int) -> int:
        return tools.remap(value, cls.MIN, cls.MAX, out_min, out_max)
