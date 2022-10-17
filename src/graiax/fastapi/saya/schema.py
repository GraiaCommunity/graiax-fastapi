from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
)

from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.params import Depends
from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id
from graia.saya.schema import BaseSchema
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

Method = Literal["GET", "PUT", "POST", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]


@dataclass
class RouteSchema(BaseSchema):
    path: str
    methods: Union[List[Method], Set[Method]]
    response_model: Any = None
    status_code: Optional[int] = None
    tags: Optional[List[Union[str, Enum]]] = None
    dependencies: Optional[Sequence[Depends]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    response_description: str = "Successful Response"
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    deprecated: Optional[bool] = None
    operation_id: Optional[str] = None
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: Type[Response] = field(default=JSONResponse)
    name: Optional[str] = None
    route_class_override: Optional[Type[APIRoute]] = None
    callbacks: Optional[List[BaseRoute]] = None
    openapi_extra: Optional[Dict[str, Any]] = None
    generate_unique_id_function: Callable[[APIRoute], str] = field(
        default=generate_unique_id
    )


@dataclass
class WebsocketRouteSchema(BaseSchema):
    path: str
    name: Optional[str] = None
