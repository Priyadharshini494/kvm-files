import sys
import os
import getpass
import tempfile
import contextlib
import textwrap
import argparse

from typing import Generator

import passlib.apache

from ...yamlconf import Section

from ...validators import ValidatorError
from ...validators.auth import valid_user
from ...validators.auth import valid_passwd

from .. import init


# =====
def _get_htpasswd_path(config: Section) -> str:
    if config.rutomatrix.auth.internal.type != "htpasswd":
        raise SystemExit(f"Error: Rutomatrix internal auth not using 'htpasswd'"
                         f" (now configured {config.rutomatrix.auth.internal.type!r})")
    return config.rutomatrix.auth.internal.file


@contextlib.contextmanager
def _get_htpasswd_for_write(config: Section) -> Generator[passlib.apache.HtpasswdFile, None, None]:
    path = _get_htpasswd_path(config)
    (tmp_fd, tmp_path) = tempfile.mkstemp(
        prefix=f".{os.path.basename(path)}.",
        dir=os.path.dirname(path),
    )
    try:
        try:
            st = os.stat(path)
            with open(path, "rb") as file:
                os.write(tmp_fd, file.read())
                os.fchown(tmp_fd, st.st_uid, st.st_gid)
                os.fchmod(tmp_fd, st.st_mode)
        finally:
            os.close(tmp_fd)
        htpasswd = passlib.apache.HtpasswdFile(tmp_path)
        yield htpasswd
        htpasswd.save()
        os.rename(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def _print_invalidate_tip(prepend_nl: bool) -> None:
    if sys.stdout.isatty() and sys.stderr.isatty():
        gray = "\033[30;1m"
        blue = "\033[34m"
        reset = "\033[39m"
    else:
        gray = blue = reset = ""
    if prepend_nl:
        print(file=sys.stderr)
    print(textwrap.dedent(f"""
        {gray}# Note: Users logged in with this username will stay logged in.
        # To invalidate their cookies you need to restart rutomatrix & rutomatrix-nginx:
        #    {reset}{blue}systemctl restart rutomatrix rutomatrix-nginx{gray}
        # Be careful, this will break your connection to the Rutomatrix
        # and may affect the GPIO relays state. Also don't forget to edit
        # the files {reset}{blue}/etc/rutomatrix/{{vncpasswd,ipmipasswd}}{gray} and restart
        # the corresponding services {reset}{blue}rutomatrix-vnc{gray} & {reset}{blue}rutomatrix-ipmi{gray} if necessary.{reset}
    """).strip(), file=sys.stderr)


# ====
def _cmd_list(config: Section, _: argparse.Namespace) -> None:
    for user in sorted(passlib.apache.HtpasswdFile(_get_htpasswd_path(config)).users()):
        print(user)


def _cmd_set(config: Section, options: argparse.Namespace) -> None:
    with _get_htpasswd_for_write(config) as htpasswd:
        has_user = (options.user in htpasswd.users())
        if options.read_stdin:
            passwd = valid_passwd(input())
        else:
            passwd = valid_passwd(getpass.getpass("Password: ", stream=sys.stderr))
            if valid_passwd(getpass.getpass("Repeat: ", stream=sys.stderr)) != passwd:
                raise SystemExit("Sorry, passwords do not match")
        htpasswd.set_password(options.user, passwd)
    if has_user and not options.quiet:
        _print_invalidate_tip(True)


def _cmd_delete(config: Section, options: argparse.Namespace) -> None:
    with _get_htpasswd_for_write(config) as htpasswd:
        has_user = (options.user in htpasswd.users())
        htpasswd.delete(options.user)
    if has_user and not options.quiet:
        _print_invalidate_tip(False)


# =====
def main(argv: (list[str] | None)=None) -> None:
    (parent_parser, argv, config) = init(
        add_help=False,
        cli_logging=True,
        argv=argv,
        load_auth=True,
    )
    parser = argparse.ArgumentParser(
        prog="Rutomatrix-htpasswd",
        description="Manage Rutomatrix users (htpasswd auth only)",
        parents=[parent_parser],
    )
    parser.set_defaults(cmd=(lambda *_: parser.print_help()))
    subparsers = parser.add_subparsers()

    cmd_list_parser = subparsers.add_parser("list", help="List users")
    cmd_list_parser.set_defaults(cmd=_cmd_list)

    cmd_set_parser = subparsers.add_parser("set", help="Create user or change password")
    cmd_set_parser.add_argument("user", type=valid_user)
    cmd_set_parser.add_argument("-i", "--read-stdin", action="store_true", help="Read password from stdin")
    cmd_set_parser.add_argument("-q", "--quiet", action="store_true", help="Don't show invalidation note")
    cmd_set_parser.set_defaults(cmd=_cmd_set)

    cmd_delete_parser = subparsers.add_parser("del", help="Delete user")
    cmd_delete_parser.add_argument("user", type=valid_user)
    cmd_delete_parser.add_argument("-q", "--quiet", action="store_true", help="Don't show invalidation note")
    cmd_delete_parser.set_defaults(cmd=_cmd_delete)

    options = parser.parse_args(argv[1:])
    try:
        options.cmd(config, options)
    except ValidatorError as err:
        raise SystemExit(str(err))
