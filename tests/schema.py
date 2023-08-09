import contextlib

from fastapi.responses import PlainTextResponse
from graia.broadcast.builtin.event import ExceptionThrown
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from graia.saya.event import SayaModuleInstalled
from launart import Launart
from pydantic import BaseModel

from graiax.fastapi import RouteSchema, route
from graiax.fastapi.interface import FastAPIProvider

channel = Channel.current()


class ResponseModel(BaseModel):
    code: int
    message: str


@channel.use(ListenerSchema([ExceptionThrown]))
async def handle_exc(exc: Exception):
    ...


@channel.use(ListenerSchema([SayaModuleInstalled]))
async def test_launart(install_channel: Channel):
    if install_channel != channel:
        return
    launart = Launart.current()
    fastapi = launart.get_interface(FastAPIProvider)

    async def interface_test():
        return PlainTextResponse("I'm from interface!")

    fastapi.add_api_route("/interface", fastapi.get("/interface")(interface_test))


@route.get("/", response_model=ResponseModel)
async def root():
    return {"code": 200, "message": "Hello World!"}


@route.route(["GET"], "/route_test")
async def route_test():
    return "@route.route(['GET'], '/route_test')"


@route.get("/route_add_test")
async def route_add_test():
    return "@route.get('/route_add_test')"


@channel.use(RouteSchema("/schema_test", methods=["GET", "POST"]))
async def schema_test():
    return "@channel.use(RouteSchema('/schema_test', methods=['GET', 'POST']))"


with contextlib.suppress(ModuleNotFoundError):
    from fastapi import WebSocket
    from starlette.websockets import WebSocketDisconnect
    from websockets.exceptions import ConnectionClosedOK

    @route.ws("/ws")
    async def ws(websocket: WebSocket):
        await websocket.accept()
        while True:
            try:
                print(await websocket.receive_text())
            except (WebSocketDisconnect, ConnectionClosedOK, RuntimeError):
                break
