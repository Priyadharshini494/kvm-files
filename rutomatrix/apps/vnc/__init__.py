from ...clients.rutomatrix import RutomatrixClient
from ...clients.streamer import StreamFormats
from ...clients.streamer import BaseStreamerClient
from ...clients.streamer import HttpStreamerClient
from ...clients.streamer import MemsinkStreamerClient

from ... import htclient

from .. import init

from .vncauth import VncAuthManager
from .server import VncServer


# =====
def main(argv: (list[str] | None)=None) -> None:
    config = init(
        prog="rutomatrix-vnc",
        description="VNC to Rutomatrix proxy",
        check_run=True,
        argv=argv,
    )[2].vnc

    user_agent = htclient.make_user_agent("Rutomatrix-VNC")

    def make_memsink_streamer(name: str, fmt: int) -> (MemsinkStreamerClient | None):
        if getattr(config.memsink, name).sink:
            return MemsinkStreamerClient(name.upper(), fmt, **getattr(config.memsink, name)._unpack())
        return None

    streamers: list[BaseStreamerClient] = list(filter(None, [
        make_memsink_streamer("h264", StreamFormats.H264),
        make_memsink_streamer("jpeg", StreamFormats.JPEG),
        HttpStreamerClient(name="JPEG", user_agent=user_agent, **config.streamer._unpack()),
    ]))

    VncServer(
        host=config.server.host,
        port=config.server.port,
        max_clients=config.server.max_clients,

        no_delay=config.server.no_delay,

        tls_ciphers=config.server.tls.ciphers,
        tls_timeout=config.server.tls.timeout,
        x509_cert_path=config.server.tls.x509.cert,
        x509_key_path=config.server.tls.x509.key,

        desired_fps=config.desired_fps,
        mouse_output=config.mouse_output,
        keymap_path=config.keymap,

        rutomatrix=RuntimeError(user_agent=user_agent, **config.rutomatrix._unpack()),
        streamers=streamers,
        vnc_auth_manager=VncAuthManager(**config.auth.vncauth._unpack()),

        **config.server.keepalive._unpack(),
        **config.auth.vencrypt._unpack(),
    ).run()
