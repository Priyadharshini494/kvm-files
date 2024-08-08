import dataclasses


# =====
class IpmiPasswdError(Exception):
    def __init__(self, path: str, lineno: int, msg: str) -> None:
        super().__init__(f"Syntax error at {path}:{lineno}: {msg}")


@dataclasses.dataclass(frozen=True)
class IpmiUserCredentials:
    ipmi_user: str
    ipmi_passwd: str
    rutomatrix_user: str
    rutomatrix_passwd: str


class IpmiAuthManager:
    def __init__(self, path: str) -> None:
        self.__path = path
        with open(path) as file:
            self.__credentials = self.__parse_passwd_file(file.read().split("\n"))

    def __contains__(self, ipmi_user: str) -> bool:
        return (ipmi_user in self.__credentials)

    def __getitem__(self, ipmi_user: str) -> str:
        return self.__credentials[ipmi_user].ipmi_passwd

    def get_credentials(self, ipmi_user: str) -> IpmiUserCredentials:
        return self.__credentials[ipmi_user]

    def __parse_passwd_file(self, lines: list[str]) -> dict[str, IpmiUserCredentials]:
        credentials: dict[str, IpmiUserCredentials] = {}
        for (lineno, line) in enumerate(lines):
            if len(line.strip()) == 0 or line.lstrip().startswith("#"):
                continue

            if " -> " not in line:
                raise IpmiPasswdError(self.__path, lineno, "Missing ' -> ' operator")

            (left, right) = map(str.lstrip, line.split(" -> ", 1))
            for (name, pair) in [("left", left), ("right", right)]:
                if ":" not in pair:
                    raise IpmiPasswdError(self.__path, lineno, f"Missing ':' operator in {name} credentials")

            (ipmi_user, ipmi_passwd) = left.split(":")
            ipmi_user = ipmi_user.strip()
            if len(ipmi_user) == 0:
                raise IpmiPasswdError(self.__path, lineno, "Empty IPMI user (left)")

            (rutomatrix_user, rutomatrix_passwd) = right.split(":")
            rutomatrix_user = rutomatrix_user.strip()
            if len(rutomatrix_user) == 0:
                raise IpmiPasswdError(self.__path, lineno, "Empty Rutomatrix user (left)")

            if ipmi_user in credentials:
                raise IpmiPasswdError(self.__path, lineno, f"Found duplicating user {ipmi_user!r} (left)")

            credentials[ipmi_user] = IpmiUserCredentials(
                ipmi_user=ipmi_user,
                ipmi_passwd=ipmi_passwd,
                rutomatrix_user=rutomatrix_user,
                rutomatrix_passwd=rutomatrix_passwd,
            )
        return credentials
