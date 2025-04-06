from abc import ABC, abstractmethod


class Resolver(ABC):
    @abstractmethod
    async def resolve[TDependency](
        self, dependency_type: type[TDependency]
    ) -> TDependency: ...
