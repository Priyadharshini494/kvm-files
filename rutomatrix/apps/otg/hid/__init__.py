import dataclasses


# =====
@dataclasses.dataclass(frozen=True)
class Hid:
    protocol: int
    subclass: int
    report_length: int
    report_descriptor: bytes
