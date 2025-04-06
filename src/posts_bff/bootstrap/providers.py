from collections.abc import AsyncIterator

from dishka import (
    Provider,
    Scope,
    WithParents,
    from_context,
    provide,
    provide_all,
)
from httpx import AsyncClient
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from posts_bff.application.queries.load_post_by_id import (
    LoadPostById,
    LoadPostByIdHandler,
)
from posts_bff.application.queries.load_posts import LoadPosts, LoadPostsHandler
from posts_bff.bootstrap.config import ServicesConfig
from posts_bff.infrastructure.post_gateway import ApiPostGateway
from posts_bff.infrastructure.post_loader import PostLoader
from posts_bff.infrastructure.profile_loader import ProfileLoader
from posts_bff.infrastructure.query_bus.dishka_resolver import DishkaResolver
from posts_bff.infrastructure.query_bus.query_sender import QuerySender
from posts_bff.infrastructure.query_bus.registry import HandlersRegistry


class ApiConfigProvider(Provider):
    scope = Scope.APP

    service_config_provider = from_context(ServicesConfig)


class HttpxProvider(Provider):
    scope = Scope.APP

    @provide(provides=AsyncClient)
    async def async_client(self) -> AsyncIterator[AsyncClient]:
        async with AsyncClient() as client:
            yield client


class ApplicationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    post_gateway = provide(WithParents[ApiPostGateway])  # type: ignore[misc]

    @provide
    def profile_loader(
        self, config: ServicesConfig, client: AsyncClient
    ) -> ProfileLoader:
        return ProfileLoader(client=client, profile_api_url=config.profile_service_url)

    @provide
    def post_loader(self, config: ServicesConfig, client: AsyncClient) -> PostLoader:
        return PostLoader(client=client, posts_api_url=config.post_service_url)


class ApplicationHandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(LoadPostsHandler, LoadPostByIdHandler)


class QueryBusProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def registry(self) -> HandlersRegistry:
        registry = HandlersRegistry()

        registry.add_query_handler(LoadPosts, LoadPostsHandler)
        registry.add_query_handler(LoadPostById, LoadPostByIdHandler)

        return registry

    resolver = provide(WithParents[DishkaResolver])  # type: ignore[misc]
    sender = provide(WithParents[QuerySender])  # type: ignore[misc]


class CliConfigProvider(Provider):
    scope = Scope.APP

    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)
