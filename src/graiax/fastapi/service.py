from __future__ import annotations

from fastapi import FastAPI
from launart import Launart, Service
from launart.utilles import any_completed

from .interface import FastAPIProvider


class FastAPIService(Service):
    id = "http.server/graiax.fastapi"
    required: set[str] = {"asgi.service/uvicorn"}
    stages: set[str] = {"blocking"}
    supported_interface_types: set = {FastAPIProvider}

    def __init__(self, fastapi: FastAPI | None = None) -> None:
        self.fastapi = fastapi or FastAPI()
        super().__init__()

    def get_interface(self, _: type[FastAPIProvider]):
        return FastAPIProvider(self, self.fastapi)

    async def launch(self, manager: Launart):
        async with self.stage("blocking"):
            await any_completed(manager.status.wait_for_sigexit())
