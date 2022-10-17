from dataclasses import asdict
from typing import Literal, Union

from fastapi import FastAPI
from fastapi.routing import APIRoute, APIWebSocketRoute
from graia.saya.behaviour import Behaviour
from graia.saya.cube import Cube

from .schema import RouteSchema, WebsocketRouteSchema


class FastAPIBehaviour(Behaviour):
    fastapi: FastAPI

    def __init__(self, fastapi: FastAPI) -> None:
        self.fastapi = fastapi

    def allocate(self, cube: Cube) -> Union[None, Literal[True]]:
        if isinstance(cube.metaclass, RouteSchema):
            self.fastapi.router.add_api_route(
                endpoint=cube.content, **asdict(cube.metaclass)
            )
            return True
        elif isinstance(cube.metaclass, WebsocketRouteSchema):
            self.fastapi.router.add_api_websocket_route(
                endpoint=cube.content,
                path=cube.metaclass.path,
                name=cube.metaclass.name,
            )
            return True

    def release(self, cube: Cube) -> Union[None, Literal[True]]:
        if not (isinstance(cube.metaclass, (RouteSchema, WebsocketRouteSchema))):
            return
        for route in self.fastapi.routes:
            if (
                isinstance(route, (APIRoute, APIWebSocketRoute))
                and route.path
                in [
                    cube.metaclass.path,
                    f"{self.fastapi.router.prefix}{cube.metaclass.path}",
                ]
                and route.endpoint == cube.content
            ):
                self.fastapi.routes.remove(route)
        return True
