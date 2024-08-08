import asyncio

from aiohttp.web import Request
from aiohttp.web import Response

from ....htserver import HttpError
from ....htserver import exposed_http
from ....htserver import make_json_response

from ....plugins.atx import BaseAtx

from ....validators import ValidatorError
from ....validators import check_string_in_list

from ..info import InfoManager


# =====
class RedfishApi:
    # https://github.com/DMTF/Redfishtool
    # https://github.com/DMTF/Redfish-Mockup-Server
    # https://redfish.dmtf.org/redfish/v1
    # https://www.dmtf.org/documents/redfish-spmf/redfish-mockup-bundle-20191
    # https://www.dmtf.org/sites/default/files/Redfish_School-Sessions.pdf
    # https://www.ibm.com/support/knowledgecenter/POWER9/p9ej4/p9ej4_kickoff.htm
    #
    # Quick examples:
    #    redfishtool -S Never -u admin -p admin -r localhost:8080 Systems
    #    redfishtool -S Never -u admin -p admin -r localhost:8080 Systems reset ForceOff

    def __init__(self, info_manager: InfoManager, atx: BaseAtx) -> None:
        self.__info_manager = info_manager
        self.__atx = atx

        self.__actions = {
            "On": self.__atx.power_on,
            "ForceOff": self.__atx.power_off_hard,
            "GracefulShutdown": self.__atx.power_off,
            "ForceRestart": self.__atx.power_reset_hard,
            "ForceOn": self.__atx.power_on,
            "PushPowerButton": self.__atx.click_power,
        }

    # =====

    @exposed_http("GET", "/redfish/v1", auth_required=False)
    async def __root_handler(self, _: Request) -> Response:
        return make_json_response({
            "@odata.id": "/redfish/v1",
            "@odata.type": "#ServiceRoot.v1_6_0.ServiceRoot",
            "Id": "RootService",
            "Name": "Root Service",
            "RedfishVersion": "1.6.0",
            "Systems": {"@odata.id": "/redfish/v1/Systems"},
        }, wrap_result=False)

    @exposed_http("GET", "/redfish/v1/Systems")
    async def __systems_handler(self, _: Request) -> Response:
        return make_json_response({
            "@odata.id": "/redfish/v1/Systems",
            "@odata.type": "#ComputerSystemCollection.ComputerSystemCollection",
            "Members": [{"@odata.id": "/redfish/v1/Systems/0"}],
            "Members@odata.count": 1,
            "Name": "Computer System Collection",
        }, wrap_result=False)

    @exposed_http("GET", "/redfish/v1/Systems/0")
    async def __server_handler(self, _: Request) -> Response:
        (atx_state, meta_state) = await asyncio.gather(*[
            self.__atx.get_state(),
            self.__info_manager.get_submanager("meta").get_state(),
        ])
        try:
            host = str(meta_state.get("server", {})["host"])  # type: ignore
        except Exception:
            host = ""
        return make_json_response({
            "@odata.id": "/redfish/v1/Systems/0",
            "@odata.type": "#ComputerSystem.v1_10_0.ComputerSystem",
            "Actions": {
                "#ComputerSystem.Reset": {
                    "ResetType@Redfish.AllowableValues": list(self.__actions),
                    "target": "/redfish/v1/Systems/0/Actions/ComputerSystem.Reset"
                },
            },
            "Id": "0",
            "HostName": host,
            "PowerState": ("On" if atx_state["leds"]["power"] else "Off"),  # type: ignore
        }, wrap_result=False)

    @exposed_http("POST", "/redfish/v1/Systems/0/Actions/ComputerSystem.Reset")
    async def __power_handler(self, request: Request) -> Response:
        try:
            action = check_string_in_list(
                arg=(await request.json())["ResetType"],
                name="Redfish ResetType",
                variants=set(self.__actions),
                lower=False,
            )
        except ValidatorError:
            raise
        except Exception:
            raise HttpError("Missing Redfish ResetType", 400)
        await self.__actions[action](False)
        return Response(body=None, status=204)
