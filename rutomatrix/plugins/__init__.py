import importlib
import functools

from typing import Any


# =====
class UnknownPluginError(Exception):
    pass


# =====
class BasePlugin:
    def __init__(self, **_: Any) -> None:
        pass  # pragma: nocover

    @classmethod
    def get_plugin_name(cls) -> str:
        name = cls.__module__
        return name[name.rindex(".") + 1:]

    @classmethod
    def get_plugin_options(cls) -> dict:
        return {}  # pragma: nocover


@functools.lru_cache()
def get_plugin_class(sub: str, name: str) -> type[BasePlugin]:
    assert sub
    assert name
    if name.startswith("_"):
        raise UnknownPluginError(f"Unknown plugin '{sub}/{name}'")
    try:
        module = importlib.import_module(f"rutomatrix.plugins.{sub}.{name}")
    except ModuleNotFoundError:
        raise UnknownPluginError(f"Unknown plugin '{sub}/{name}'")
    return getattr(module, "Plugin")
