import types

from typing import Any

import dbus
import dbus.proxies


# =====
HID_CTL_PORT = 17
HID_INT_PORT = 19


# =====
class BluezIface:
    # https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/profile-api.txt
    # https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    # qdbus --system org.bluez /org/bluez/hci0 org.bluez.Adapter1.Address

    def __init__(
        self,
        iface: str,
        alias: str,
        sdp_record: str,
        pairing_required: bool,
        auth_required: bool,
    ) -> None:

        self.__iface = iface
        self.__alias = alias
        self.__sdp_record = sdp_record
        self.__pairing_required = pairing_required
        self.__auth_required = auth_required

        self.__bus: (dbus.SystemBus | None) = None

    def get_address(self) -> str:
        return self.__get_prop("Address")

    def configure(self) -> None:
        self.__set_prop("Alias", self.__alias)
        manager = dbus.Interface(self.__get_object("/org/bluez"), "org.bluez.ProfileManager1")
        manager.RegisterProfile(f"/org/bluez/{self.__iface}", "00001124-0000-1000-8000-00805F9B34FB", {
            "ServiceRecord": self.__sdp_record,
            "Role": "server",
            "RequireAuthentication": self.__pairing_required,
            "RequireAuthorization": self.__auth_required,
        })
        self.__set_prop("Powered", True)

    def set_public(self, public: bool) -> None:
        self.__set_prop("Pairable", public)
        self.__set_prop("Discoverable", public)

    def unpair(self, addr: str) -> None:
        adapter = dbus.Interface(self.__get_object(f"/org/bluez/{self.__iface}"), "org.bluez.Adapter1")
        adapter.RemoveDevice(f"/org/bluez/hci0/dev_{addr.upper().replace(':', '_')}")

    def __get_prop(self, key: str) -> Any:
        return self.__get_props().Get("org.bluez.Adapter1", key)

    def __set_prop(self, key: str, value: Any) -> None:
        self.__get_props().Set("org.bluez.Adapter1", key, value)

    def __get_props(self) -> dbus.Interface:
        return dbus.Interface(self.__get_object(f"/org/bluez/{self.__iface}"), "org.freedesktop.DBus.Properties")

    def __get_object(self, path: str) -> dbus.proxies.ProxyObject:
        assert self.__bus is not None
        return self.__bus.get_object("org.bluez", path)

    def __enter__(self) -> "BluezIface":
        assert self.__bus is None
        self.__bus = dbus.SystemBus()
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException],
        _exc: BaseException,
        _tb: types.TracebackType,
    ) -> None:

        assert self.__bus is not None
        self.__bus.close()
        self.__bus = None
