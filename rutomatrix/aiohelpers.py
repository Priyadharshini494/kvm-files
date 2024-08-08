import subprocess

from .logging import get_logger

from . import tools
from . import aioproc


# =====
async def remount(name: str, base_cmd: list[str], rw: bool) -> bool:
    logger = get_logger(1)
    mode = ("rw" if rw else "ro")
    cmd = [
        part.format(mode=mode)
        for part in base_cmd
    ]
    logger.info("Remounting %s storage to %s: %s ...", name, mode.upper(), tools.cmdfmt(cmd))
    try:
        proc = await aioproc.log_process(cmd, logger)
        if proc.returncode != 0:
            assert proc.returncode is not None
            raise subprocess.CalledProcessError(proc.returncode, cmd)
    except Exception as err:
        logger.error("Can't remount %s storage: %s", name, tools.efmt(err))
        return False
    return True
