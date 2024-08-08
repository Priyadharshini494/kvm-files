import dataclasses

from ...logging import get_logger

from ... import aiotools


# =====
class VncAuthError(Exception):
    def __init__(self, path: str, lineno: int, msg: str) -> None:
        super().__init__(f"Syntax error at {path}:{lineno}: {msg}")


# =====
@dataclasses.dataclass(frozen=True)
class VncAuthRutomatrixCredentials:
    user: str
    passwd: str


class VncAuthManager:
    def __init__(
        self,
        path: str,
        enabled: bool,
    ) -> None:

        self.__path = path
        self.__enabled = enabled

    async def read_credentials(self) -> tuple[dict[str, VncAuthRutomatrixCredentials], bool]:
        if self.__enabled:
            try:
                return (await self.__inner_read_credentials(), True)
            except VncAuthError as err:
                get_logger(0).error(str(err))
            except Exception:
                get_logger(0).exception("Unhandled exception while reading VNCAuth passwd file")
        return ({}, (not self.__enabled))

    async def __inner_read_credentials(self) -> dict[str, VncAuthRutomatrixCredentials]:
        lines = (await aiotools.read_file(self.__path)).split("\n")
        credentials: dict[str, VncAuthRutomatrixCredentials] = {}
        for (lineno, line) in enumerate(lines):
            if len(line.strip()) == 0 or line.lstrip().startswith("#"):
                continue

            if " -> " not in line:
                raise VncAuthError(self.__path, lineno, "Missing ' -> ' operator")

            (vnc_passwd, rutomatrix_userpass) = map(str.lstrip, line.split(" -> ", 1))
            if ":" not in rutomatrix_userpass:
                raise VncAuthError(self.__path, lineno, "Missing ':' operator in Rutomatrix credentials (right part)")

            (rutomatrix_user, rutomatrix_passwd) = rutomatrix_userpass.split(":")
            rutomatrix_user = rutomatrix_user.strip()
            if len(rutomatrix_user) == 0:
                raise VncAuthError(self.__path, lineno, "Empty Rutomatrix user (right part)")

            if vnc_passwd in credentials:
                raise VncAuthError(self.__path, lineno, "Duplicating VNC password (left part)")

            credentials[vnc_passwd] = VncAuthRutomatrixCredentials(rutomatrix_user, rutomatrix_passwd)
        return credentials
