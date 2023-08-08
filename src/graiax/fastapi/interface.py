from __future__ import annotations

from collections.abc import Coroutine, Sequence
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable

from fastapi import FastAPI, routing
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.params import Depends
from fastapi.types import DecoratedCallable, IncEx
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

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

        def add_api_route(
            self,
            path: str,
            endpoint: Callable[..., Coroutine[Any, Any, Response]],
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            methods: list[str] | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
            name: str | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> None:
            ...

        def add_api_websocket_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            name: str | None = None,
            *,
            dependencies: Sequence[Depends] | None = None,
        ) -> None:
            ...

        def include_router(
            self,
            router: routing.APIRouter,
            *,
            prefix: str = "",
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            include_in_schema: bool = True,
            default_response_class: type[Response] = Default(JSONResponse),
            callbacks: list[BaseRoute] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> None:
            ...

        def get(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def put(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def post(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def delete(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def options(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def head(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def patch(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...

        def trace(
            self,
            path: str,
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] = Default(JSONResponse),
            name: str | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(generate_unique_id),
        ) -> Callable[[DecoratedCallable], DecoratedCallable]:
            ...
