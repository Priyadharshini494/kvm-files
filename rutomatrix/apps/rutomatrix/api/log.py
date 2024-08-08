from aiohttp.web import Request
from aiohttp.web import StreamResponse

from ....errors import OperationError

from ....htserver import exposed_http
from ....htserver import start_streaming

from ....validators.basic import valid_bool
from ....validators.ruto import valid_log_seek

from ..logreader import LogReader


# =====
class LogReaderDisabledError(OperationError):
    def __init__(self) -> None:
        super().__init__("LogReader is disabled")


class LogApi:
    def __init__(self, log_reader: (LogReader | None)) -> None:
        self.__log_reader = log_reader

    # =====

    @exposed_http("GET", "/log")
    async def __log_handler(self, request: Request) -> StreamResponse:
        if self.__log_reader is None:
            raise LogReaderDisabledError()
        seek = valid_log_seek(request.query.get("seek", 0))
        follow = valid_bool(request.query.get("follow", False))
        response = await start_streaming(request, "text/plain")
        async for record in self.__log_reader.poll_log(seek, follow):
            await response.write(("[%s %s] --- %s" % (
                record["dt"].strftime("%Y-%m-%d %H:%M:%S"),
                record["service"],
                record["msg"],
            )).encode("utf-8") + b"\r\n")
        return response
