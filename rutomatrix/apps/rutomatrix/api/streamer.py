from aiohttp.web import Request
from aiohttp.web import Response

from ....htserver import UnavailableError
from ....htserver import exposed_http
from ....htserver import make_json_response

from ....validators import check_string_in_list
from ....validators.basic import valid_bool
from ....validators.basic import valid_number
from ....validators.basic import valid_int_f0
from ....validators.basic import valid_string_list
from ....validators.ruto import valid_stream_quality

from ..streamer import Streamer
from ..streamer2 import Streamer2
from ..ocr import Ocr

from ....logging import get_logger

# =====
class StreamerApi:
    def __init__(self, streamer: Streamer, ocr: Ocr) -> None:
        self.__streamer = streamer
        self.__ocr = ocr

    # =====

    @exposed_http("GET", "/streamer")
    async def __state_handler(self, _: Request) -> Response:
        logger = get_logger(0)
        logger.info("Streamer response check",await self.__streamer.get_state())
        return make_json_response(await self.__streamer.get_state())

    @exposed_http("GET", "/streamer/snapshot")
    async def __take_snapshot_handler(self, request: Request) -> Response:
        snapshot = await self.__streamer.take_snapshot(
            save=valid_bool(request.query.get("save", False)),
            load=valid_bool(request.query.get("load", False)),
            allow_offline=valid_bool(request.query.get("allow_offline", False)),
        )
        if snapshot:
            if valid_bool(request.query.get("ocr", False)):
                langs = self.__ocr.get_available_langs()
                return Response(
                    body=(await self.__ocr.recognize(
                        data=snapshot.data,
                        langs=valid_string_list(
                            arg=str(request.query.get("ocr_langs", "")).strip(),
                            subval=(lambda lang: check_string_in_list(lang, "OCR lang", langs)),
                            name="OCR langs list",
                        ),
                        left=int(valid_number(request.query.get("ocr_left", -1))),
                        top=int(valid_number(request.query.get("ocr_top", -1))),
                        right=int(valid_number(request.query.get("ocr_right", -1))),
                        bottom=int(valid_number(request.query.get("ocr_bottom", -1))),
                    )),
                    headers=dict(snapshot.headers),
                    content_type="text/plain",
                )
            elif valid_bool(request.query.get("preview", False)):
                data = await snapshot.make_preview(
                    max_width=valid_int_f0(request.query.get("preview_max_width", 0)),
                    max_height=valid_int_f0(request.query.get("preview_max_height", 0)),
                    quality=valid_stream_quality(request.query.get("preview_quality", 80)),
                )
            else:
                data = snapshot.data
            return Response(
                body=data,
                headers=dict(snapshot.headers),
                content_type="image/jpeg",
            )
        raise UnavailableError()

    @exposed_http("DELETE", "/streamer/snapshot")
    async def __remove_snapshot_handler(self, _: Request) -> Response:
        self.__streamer.remove_snapshot()
        return make_json_response()

    # =====

    async def get_ocr(self) -> dict:  # XXX: Ugly hack
        enabled = self.__ocr.is_available()
        default: list[str] = []
        available: list[str] = []
        if enabled:
            default = self.__ocr.get_default_langs()
            available = self.__ocr.get_available_langs()
        return {
            "ocr": {
                "enabled": enabled,
                "langs": {
                    "default": default,
                    "available": available,
                },
            },
        }

    @exposed_http("GET", "/streamer/ocr")
    async def __ocr_handler(self, _: Request) -> Response:
        return make_json_response(await self.get_ocr())
