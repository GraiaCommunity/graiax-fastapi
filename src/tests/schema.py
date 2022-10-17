from graia.saya import Channel
from pydantic import BaseModel

from graiax.fastapi import RouteSchema, route

channel = Channel.current()


class ResponseModel(BaseModel):
    code: int
    message: str


# 方式一：像原版 FastAPI 那样直接使用装饰器
@route.get("/", response_model=ResponseModel)
async def root():
    return {"code": 200, "message": "Hello World!"}


# 方式二：当你先需要同一个路径有多种请求方式时你可以这样做
@route.route(["GET"], "/xxxxx")
async def xxxxx():
    return "xxxx"


# 方式三：上面那种方式实际上也可以这么写
@channel.use(RouteSchema("/xxx", methods=["GET", "POST"]))
async def xxx():
    return "xxx"


# Websocket
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK


@route.ws("/ws")
# 等价于 @channel.use(WebsocketRouteSchema("/ws"))
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            print(await websocket.receive_text())
        except (WebSocketDisconnect, ConnectionClosedOK, RuntimeError):
            break
