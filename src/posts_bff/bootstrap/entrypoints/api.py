from typing import TYPE_CHECKING, cast

from dishka.integrations.fastapi import (
    setup_dishka as add_container_to_fastapi,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from posts_bff.application.common.application_error import ApplicationError
from posts_bff.bootstrap.config import get_services_config
from posts_bff.bootstrap.container import bootstrap_api_container
from posts_bff.presentation.api.exception_handlers import (
    application_error_handler,
    internal_error_handler,
)
from posts_bff.presentation.api.routers.healthcheck import HEALTHCHECK_ROUTER
from posts_bff.presentation.api.routers.posts import POSTS_ROUTER

if TYPE_CHECKING:
    from starlette.types import HTTPExceptionHandler


def add_middlewares(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


def add_api_routers(application: FastAPI) -> None:
    application.include_router(POSTS_ROUTER)
    application.include_router(HEALTHCHECK_ROUTER)


def add_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(
        ApplicationError,
        cast("HTTPExceptionHandler", application_error_handler),
    )
    application.add_exception_handler(
        Exception,
        cast("HTTPExceptionHandler", internal_error_handler),
    )


def bootstrap_application() -> FastAPI:
    application = FastAPI()
    dishka_container = bootstrap_api_container(get_services_config())

    add_middlewares(application)
    add_api_routers(application)
    add_exception_handlers(application)
    add_container_to_fastapi(dishka_container, application)

    return application
