import asyncio

from aiohttp.web import Request
from aiohttp.web import Response

from ....htserver import exposed_http
from ....htserver import make_json_response

from ....validators.ruto import valid_info_fields

from ..info import InfoManager
from ..info import InfoManager2
from ..info import InfoManager3
from ..info import InfoManager4


# =====
class InfoApi:
    def __init__(self, info_manager: InfoManager) -> None:
        self.__info_manager = info_manager

    # =====

    @exposed_http("GET", "/info")
    async def __common_state_handler(self, request: Request) -> Response:
        fields = self.__valid_info_fields(request)
        results = dict(zip(fields, await asyncio.gather(*[
            self.__info_manager.get_submanager(field).get_state()
            for field in fields
        ])))
        return make_json_response(results)

    def __valid_info_fields(self, request: Request) -> list[str]:
        subs = self.__info_manager.get_subs()
        return sorted(valid_info_fields(
            arg=request.query.get("fields", ",".join(subs)),
            variants=subs,
        ) or subs)

class InfoApi2:
    def __init__(self, info_manager: InfoManager2) -> None:
        self.__info_manager = info_manager

    # =====

    @exposed_http("GET", "/info2")
    async def __common_state_handler(self, request: Request) -> Response:
        fields = self.__valid_info_fields(request)
        results = dict(zip(fields, await asyncio.gather(*[
            self.__info_manager.get_submanager(field).get_state()
            for field in fields
        ])))
        return make_json_response(results)

    def __valid_info_fields(self, request: Request) -> list[str]:
        subs = self.__info_manager.get_subs()
        return sorted(valid_info_fields(
            arg=request.query.get("fields", ",".join(subs)),
            variants=subs,
        ) or subs)


class InfoApi3:
    def __init__(self, info_manager: InfoManager3) -> None:
        self.__info_manager = info_manager

    # =====

    @exposed_http("GET", "/info3")
    async def __common_state_handler(self, request: Request) -> Response:
        fields = self.__valid_info_fields(request)
        results = dict(zip(fields, await asyncio.gather(*[
            self.__info_manager.get_submanager(field).get_state()
            for field in fields
        ])))
        return make_json_response(results)

    def __valid_info_fields(self, request: Request) -> list[str]:
        subs = self.__info_manager.get_subs()
        return sorted(valid_info_fields(
            arg=request.query.get("fields", ",".join(subs)),
            variants=subs,
        ) or subs)


class InfoApi4:
    def __init__(self, info_manager: InfoManager4) -> None:
        self.__info_manager = info_manager

    # =====

    @exposed_http("GET", "/info4")
    async def __common_state_handler(self, request: Request) -> Response:
        fields = self.__valid_info_fields(request)
        results = dict(zip(fields, await asyncio.gather(*[
            self.__info_manager.get_submanager(field).get_state()
            for field in fields
        ])))
        return make_json_response(results)

    def __valid_info_fields(self, request: Request) -> list[str]:
        subs = self.__info_manager.get_subs()
        return sorted(valid_info_fields(
            arg=request.query.get("fields", ",".join(subs)),
            variants=subs,
        ) or subs)
