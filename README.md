<div align="center">

# GraiaX FastAPI

> :sparkles: Easy FastAPI Access for GraiaCommunity :sparkles:

[![codecov](https://codecov.io/gh/GraiaCommunity/graiax-fastapi/branch/master/graph/badge.svg?token=IU7kXPfTsV)](https://codecov.io/gh/GraiaCommunity/graiax-fastapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/github/license/GraiaCommunity/graiax-fastapi)](https://github.com/GraiaCommunity/graiax-fastapi/blob/master/LICENSE)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

</div>

你可以方便地使用 GraiaX FastAPI 配合 `graia.amnesia.builtins.uvicorn.UvicornService`
轻松地在启动使用了 Graia Amnesia 的项目（如：Ariadne、Avilla）的同时启动一个
Uvicorn 服务器并把 FastAPI 作为其 `ASGIApplication`，并在其退出的时候自动关闭 Uvicorn。

## 安装

`pdm add graiax-fastapi` 或 `poetry add graiax-fastapi`。

> 我们强烈建议使用包管理器或虚拟环境

## 开始使用

以 Ariadne 为例。

### 配合 Launart 使用

#### 机器人入口文件

如果你有使用 **Graia Saya** 作为模块管理工具，那么你可以使用 **FastAPIBehaviour**
以在 Saya 模块中更方便地使用 FastAPI。

FastAPI 本身并 **不自带** ASGI 服务器，因此你需要额外添加一个 **UvicornService**。

```python
from creart import create
from graia.ariadne.app import Ariadne
from graia.amnesia.builtins.uvicorn import UvicornService
from graiax.fastapi import FastAPIBehaviour, FastAPIService
from graia.saya import Saya

app = Ariadne(...)
saya = create(Saya)
fastapi = FastAPI()

saya.install_behaviours(FastAPIBehaviour(fastapi))

# 可以不创建 FastAPI 实例, 交给 FastAPIService 自己创建
# app.launch_manager.add_service(FastAPIService())
# 这样的话就不能给 FastAPI 传参并自定义 FastAPI
app.launch_manager.add_service(FastAPIService(fastapi))
app.launch_manager.add_service(UvicornService())

Ariadne.launch_blocking()
```

#### Saya 模块中

```python
from graia.saya import Channel
from pydantic import BaseModel

from graiax.fastapi import RouteSchema, route

channel = Channel.current()


class ResponseModel(BaseModel):
    code: int
    message: str


# 方式一：像 FastAPI 那样直接使用装饰器
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
```

#### 其他方式

假如你不想在 Saya 模块中为 FastAPI 添加路由，那么你可以选择以下几种方式：

<details>

##### 在机器人入口文件中直接添加

```python
...
fastapi = FastAPI()


@fastapi.get("/main")
async def main():
    return "main"


app.launch_manager.add_service(FastAPIService(fastapi))
...
```

##### 在 Ariadne 启动成功后添加

```python
from graia.amnesia.builtins.uvicorn import ASGIHandlerProvider


async def root():
    ...


@listen(ApplicationLaunched)
async def function(app: Ariadne):
    mgr = app.launch_manager
    fastapi: FastAPI = mgr.get_interface(ASGIHandlerProvider).get_asgi_handler()  # type: ignore
    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    fastapi.add_api_route('/', endpoint=root, methods=['GET'])
    fastapi.get('/main')(root)
    fastapi.add_api_websocket_route('/ws', endpoint=websocket)
```

</details>
