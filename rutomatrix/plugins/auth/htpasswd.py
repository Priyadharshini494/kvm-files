import passlib.apache

from ...yamlconf import Option

from ...validators.os import valid_abs_file

from . import BaseAuthService


# =====
class Plugin(BaseAuthService):
    def __init__(self, path: str) -> None:  # pylint: disable=super-init-not-called
        self.__path = path

    @classmethod
    def get_plugin_options(cls) -> dict:
        return {
            "file": Option("/etc/rutomatrix/htpasswd", type=valid_abs_file, unpack_as="path"),
        }

    async def authorize(self, user: str, passwd: str) -> bool:
        assert user == user.strip()
        assert user
        htpasswd = passlib.apache.HtpasswdFile(self.__path)
        return htpasswd.check_password(user, passwd)
