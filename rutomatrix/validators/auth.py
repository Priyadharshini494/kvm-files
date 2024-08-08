from typing import Any

from .basic import valid_string_list

from . import check_re_match


# =====
def valid_user(arg: Any) -> str:
    return check_re_match(arg, "username characters", r"^[a-z_][a-z0-9_-]*$")


def valid_users_list(arg: Any) -> list[str]:
    return valid_string_list(arg, subval=valid_user, name="users list")


def valid_passwd(arg: Any) -> str:
    return check_re_match(arg, "passwd characters", r"^[\x20-\x7e]*\Z$", strip=False, hide=True)


def valid_auth_token(arg: Any) -> str:
    return check_re_match(arg, "auth token", r"^[0-9a-f]{64}$", hide=True)
