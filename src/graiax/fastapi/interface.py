from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

if TYPE_CHECKING:
    from .service import FastAPIService


class FastAPIProvider:
    fastapi: FastAPI
    service: FastAPIService

    def __init__(self, service: FastAPIService, fastapi: FastAPI):
        self.service = service
        self.fastapi = fastapi

        super().__init__()

    # 为了保持和旧版 Graia Amnesia 一致的用法
    def get_asgi_handler(self):
        return self.fastapi

    # 可以直接调 FastAPI 的方法
    if not TYPE_CHECKING:

        def __getattr__(self, name: str):
            return self.fastapi.__getattribute__(name)

    else:
        add_api_route = FastAPI.add_api_route
        add_api_websocket_route = FastAPI.add_api_websocket_route
        include_router = FastAPI.include_router
        get = FastAPI.get
        put = FastAPI.put
        post = FastAPI.post
        delete = FastAPI.delete
        options = FastAPI.options
        head = FastAPI.head
        patch = FastAPI.patch
        trace = FastAPI.trace
