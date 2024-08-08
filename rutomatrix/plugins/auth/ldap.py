import ldap

from ...yamlconf import Option

from ...validators.basic import valid_stripped_string_not_empty
from ...validators.basic import valid_bool
from ...validators.basic import valid_int_f1

from ...logging import get_logger

from ... import tools
from ... import aiotools

from . import BaseAuthService


# =====
class Plugin(BaseAuthService):
    def __init__(  # pylint: disable=super-init-not-called
        self,
        url: str,
        verify: bool,
        base: str,
        group: str,
        user_domain: str,
        timeout: float,
    ) -> None:

        self.__url = url
        self.__verify = verify
        self.__base = base
        self.__group = group
        self.__user_domain = user_domain
        self.__timeout = timeout

    @classmethod
    def get_plugin_options(cls) -> dict:
        return {
            "url":         Option("",   type=valid_stripped_string_not_empty),
            "verify":      Option(True, type=valid_bool),
            "base":        Option("",   type=valid_stripped_string_not_empty),
            "group":       Option("",   type=valid_stripped_string_not_empty),
            "user_domain": Option(""),
            "timeout":     Option(5, type=valid_int_f1),
        }

    async def authorize(self, user: str, passwd: str) -> bool:
        return (await aiotools.run_async(self.__inner_authorize, user, passwd))

    def __inner_authorize(self, user: str, passwd: str) -> bool:
        if self.__user_domain:
            user = f"{user}@{self.__user_domain}"
        conn: (ldap.ldapobject.LDAPObject | None) = None
        try:
            conn = ldap.initialize(self.__url)
            conn.set_option(ldap.OPT_REFERRALS, 0)
            conn.set_option(ldap.OPT_TIMEOUT, self.__timeout)
            if self.__url.lower().startswith("ldaps://"):
                conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
                conn.set_option(ldap.OPT_X_TLS_DEMAND, True)
                if not self.__verify:
                    conn.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
                conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
            conn.simple_bind_s(user, passwd)
            for (dn, attrs) in (conn.search_st(
                base=self.__base,
                scope=ldap.SCOPE_SUBTREE,
                filterstr=f"(&(objectClass=user)(userPrincipalName={user})(memberOf={self.__group}))",
                attrlist=["memberOf"],
                timeout=self.__timeout,
            ) or []):
                if (
                    dn is not None
                    and isinstance(attrs, dict)
                    and isinstance(attrs["memberOf"], (list, dict))
                    and self.__group.encode() in attrs["memberOf"]
                ):
                    return True
        except ldap.INVALID_CREDENTIALS:
            pass
        except ldap.SERVER_DOWN as err:
            get_logger().error("LDAP server is down: %s", tools.efmt(err))
        except Exception as err:
            get_logger().error("Unexpected LDAP error: %s", tools.efmt(err))
        finally:
            if conn is not None:
                try:
                    conn.unbind()
                except Exception:
                    pass
        return False
