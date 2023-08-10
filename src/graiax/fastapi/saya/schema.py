from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Literal, Sequence

from fastapi import routing
from fastapi.params import Depends
from fastapi.types import IncEx
from fastapi.utils import generate_unique_id
from graia.saya.schema import BaseSchema
from starlette.responses import JSONResponse, Response

Method = Literal["GET", "PUT", "POST", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]


@dataclass
class RouteSchema(BaseSchema):
    path: str
    methods: list[Method]
    response_model: Any = None
    status_code: int | None = None
    tags: list[str | Enum] | None = None
    dependencies: Sequence[Depends] | None = None
    summary: str | None = None
    description: str | None = None
    response_description: str = "Successful Response"
    responses: dict[int | str, dict[str, Any]] | None = None
    deprecated: bool | None = None
    operation_id: str | None = None
    response_model_include: IncEx | None = None
    response_model_exclude: IncEx | None = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: type[Response] = field(default=JSONResponse)
    name: str | None = None
    openapi_extra: dict[str, Any] | None = None
    generate_unique_id_function: Callable[[routing.APIRoute], str] = field(default=generate_unique_id)


@dataclass
class WebsocketRouteSchema(BaseSchema):
    path: str
    name: str | None = None
    dependencies: Sequence[Depends] | None = None
