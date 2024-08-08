from .... import tools


# =====
class RfbError(Exception):
    pass


class RfbConnectionError(RfbError):
    def __init__(self, msg: str, err: Exception) -> None:
        super().__init__(f"{msg}: {tools.efmt(err)}")
