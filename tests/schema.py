from graia.broadcast.builtin.event import ExceptionThrown
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from pydantic import BaseModel

from graiax.fastapi import RouteSchema, route

channel = Channel.current()


class ResponseModel(BaseModel):
    code: int
    message: str


@channel.use(ListenerSchema([ExceptionThrown]))
async def handle_exc(exc: Exception):
    ...


@route.get("/", response_model=ResponseModel)
@route.get(
    "/", response_model=ResponseModel
)  # duplication will be automatically removed
async def root():
    return {"code": 200, "message": "Hello World!"}


@route.route(["GET"], "/xxxxx")
async def xxxxx():
    return "xxxx"


@channel.use(RouteSchema("/xxx", methods=["GET", "POST"]))
async def xxx():
    return "xxx"


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
