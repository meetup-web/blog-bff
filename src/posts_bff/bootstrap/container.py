from dishka import (
    AsyncContainer,
    Container,
    make_async_container,
    make_container,
)
from dishka.integrations.fastapi import FastapiProvider
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from posts_bff.bootstrap.config import ServicesConfig
from posts_bff.bootstrap.providers import (
    ApiConfigProvider,
    ApplicationAdaptersProvider,
    ApplicationHandlersProvider,
    CliConfigProvider,
    HttpxProvider,
    QueryBusProvider,
)


def bootstrap_api_container(services_config: ServicesConfig) -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        ApiConfigProvider(),
        HttpxProvider(),
        QueryBusProvider(),
        ApplicationAdaptersProvider(),
        ApplicationHandlersProvider(),
        context={
            ServicesConfig: services_config,
        },
    )


def bootstrap_cli_container(
    uvicorn_config: UvicornConfig,
    uvicorn_server: UvicornServer,
) -> Container:
    return make_container(
        CliConfigProvider(),
        context={
            UvicornConfig: uvicorn_config,
            UvicornServer: uvicorn_server,
        },
    )
