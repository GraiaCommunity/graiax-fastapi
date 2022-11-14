from graia.saya import Channel
from pydantic import BaseModel

from graiax.fastapi import RouteSchema, route

channel = Channel.current()


class ResponseModel(BaseModel):
    code: int
    message: str


# 如果有 graia.broadcast 可以捕获运行中出现的部分错误并对其进行处理

# from graia.saya.builtins.broadcast import ListenerSchema  # noqa: E402
# from graia.broadcast.builtin.event import ExceptionThrown  # noqa: E402

# @channel.use(ListenerSchema([ExceptionThrown]))
# async def handle_exc(exc: Exception):
#     ...


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


from fastapi import WebSocket  # noqa: E402
from starlette.websockets import WebSocketDisconnect  # noqa: E402
from websockets.exceptions import ConnectionClosedOK  # noqa: E402


@route.ws("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            print(await websocket.receive_text())
        except (WebSocketDisconnect, ConnectionClosedOK, RuntimeError):
            break
