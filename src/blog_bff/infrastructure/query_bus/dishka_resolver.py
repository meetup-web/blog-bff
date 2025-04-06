from dishka import AsyncContainer

from blog_bff.infrastructure.query_bus.adapters.resolver import Resolver


class DishkaResolver(Resolver):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve[TDependency](
        self, dependency_type: type[TDependency]
    ) -> TDependency:
        return await self._container.get(dependency_type)
