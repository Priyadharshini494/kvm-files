from .. import init

from .runner import JanusRunner


# =====
def main(argv: (list[str] | None)=None) -> None:
    config = init(
        prog="rutomatrix-Janus",
        description="Janus WebRTC Gateway Runner",
        check_run=True,
        argv=argv,
    )[2].janus

    JanusRunner(
        **config.stun._unpack(),
        **config.check._unpack(),
        **config._unpack(ignore=["stun", "check"]),
    ).run()
