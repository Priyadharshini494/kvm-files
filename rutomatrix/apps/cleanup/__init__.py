import signal
import time

import psutil

from ...logging import get_logger

from ...yamlconf import Section

from .. import init


# =====
def _kill_streamer(config: Section) -> None:
    logger = get_logger(0)

    if config.streamer.process_name_prefix:
        prefix = config.streamer.process_name_prefix + ":"
        logger.info("Trying to find and kill the streamer %r ...", prefix + " <app>")

        for proc in psutil.process_iter():
            attrs = proc.as_dict(attrs=["name"])
            if attrs.get("name", "").startswith(prefix):
                try:
                    proc.send_signal(signal.SIGTERM)
                except Exception:
                    logger.exception("Can't send SIGTERM to streamer with pid=%d", proc.pid)
                time.sleep(3)
                if proc.is_running():
                    try:
                        proc.send_signal(signal.SIGKILL)
                    except Exception:
                        logger.exception("Can't send SIGKILL to streamer with pid=%d", proc.pid)


# =====
def main(argv: (list[str] | None)=None) -> None:
    config = init(
        prog="Rutomatrix-cleanup",
        description="Kill Rutomatrix and clear resources",
        check_run=True,
        argv=argv,
    )[2].Rutomatrix

    logger = get_logger(0)
    logger.info("Cleaning up ...")

    try:
        _kill_streamer(config)
    except Exception:
        pass

    logger.info("Bye-bye")
