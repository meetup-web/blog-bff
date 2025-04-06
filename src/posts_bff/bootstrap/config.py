from dataclasses import dataclass
from os import environ

from uvicorn import Config as UvicornConfig

DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 8000
DEFAULT_POST_SERVICE_URL = "http://127.0.0.1:8001"
DEFAULT_PROFILE_SERVICE_URL = "http://127.0.0.1:8002"


@dataclass(frozen=True)
class ServicesConfig:
    post_service_url: str
    profile_service_url: str


def get_uvicorn_config() -> UvicornConfig:
    return UvicornConfig(
        environ.get(
            "SERVER_FACTORY_PATH",
            "posts_bff.bootstrap.entrypoints.api:bootstrap_application",
        ),
        environ.get("SERVER_HOST", DEFAULT_SERVER_HOST),
        int(environ.get("SERVER_PORT", DEFAULT_SERVER_PORT)),
        factory=True,
    )


def get_services_config() -> ServicesConfig:
    return ServicesConfig(
        environ.get("POST_SERVICE_URL", DEFAULT_POST_SERVICE_URL),
        environ.get("PROFILE_SERVICE_URL", DEFAULT_PROFILE_SERVICE_URL),
    )
