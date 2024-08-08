import os

from . import env


# =====
def find_udc(udc: str) -> str:
    path = f"{env.SYSFS_PREFIX}/sys/class/udc"
    candidates = sorted(os.listdir(path))
    if not udc:
        if len(candidates) == 0:
            raise RuntimeError("Can't find any UDC")
        udc = candidates[0]
    elif udc not in candidates:
        raise RuntimeError(f"Can't find selected UDC: {udc}")
    return udc  # fe980000.usb


# =====
U_STATE = "state"


def get_udc_path(udc: str, *parts: str) -> str:
    return os.path.join(f"{env.SYSFS_PREFIX}/sys/class/udc", udc, *parts)


# =====
G_UDC = "UDC"
G_FUNCTIONS = "functions"
G_PROFILE_NAME = "c.1"
G_PROFILE = f"configs/{G_PROFILE_NAME}"


def get_gadget_path(gadget: str, *parts: str) -> str:
    return os.path.join(f"{env.SYSFS_PREFIX}/sys/kernel/config/usb_gadget", gadget, *parts)
