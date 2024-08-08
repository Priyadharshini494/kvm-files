from ...clients.rutomatrix import RutomatrixClient

from ... import htclient

from .. import init

from .auth import IpmiAuthManager
from .server import IpmiServer


# =====
def main(argv: (list[str] | None)=None) -> None:
    config = init(
        prog="Rutomatrix-ipmi",
        description="IPMI to Rutomatrix proxy",
        check_run=True,
        argv=argv,
    )[2].ipmi

    IpmiServer(
        auth_manager=IpmiAuthManager(**config.auth._unpack()),
        rutomatrix=RutomatrixClient(
            user_agent=htclient.make_user_agent("Rutomatrix-IPMI"),
            **config.rutomatrix._unpack(),
        ),
        **{  # Makes mypy happy (too many arguments for IpmiServer)
            **config.server._unpack(),
            **config.sol._unpack(),
        },
    ).run()
