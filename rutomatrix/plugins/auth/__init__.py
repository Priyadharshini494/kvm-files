from .. import BasePlugin
from .. import get_plugin_class


# =====
class BaseAuthService(BasePlugin):
    async def authorize(self, user: str, passwd: str) -> bool:
        raise NotImplementedError  # pragma: nocover

    async def cleanup(self) -> None:
        pass


# =====
def get_auth_service_class(name: str) -> type[BaseAuthService]:
    return get_plugin_class("auth", name)  # type: ignore
