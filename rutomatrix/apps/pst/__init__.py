from ...logging import get_logger

from .. import init

from .server import PstServer


# =====
def main(argv: (list[str] | None)=None) -> None:
    config = init(
        prog="rutomatrix-pst",
        description="The Rutomatrix persistent storage manager",
        argv=argv,
        check_run=True,
    )[2]

    PstServer(
        **config.pst._unpack(ignore="server"),
    ).run(**config.pst.server._unpack())

    get_logger(0).info("Bye-bye")
