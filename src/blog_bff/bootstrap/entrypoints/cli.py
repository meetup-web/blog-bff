from click import Context, group, pass_context
from dishka.integrations.click import setup_dishka
from uvicorn import Server as UvicornServer

from blog_bff.bootstrap.config import get_uvicorn_config
from blog_bff.bootstrap.container import bootstrap_cli_container
from blog_bff.presentation.cli.server_starting import start_uvicorn


@group()
@pass_context
def main(context: Context) -> None:
    uvicorn_config = get_uvicorn_config()
    uvicorn_server = UvicornServer(uvicorn_config)
    dishka_container = bootstrap_cli_container(uvicorn_config, uvicorn_server)
    setup_dishka(dishka_container, context, finalize_container=True)


main.command(start_uvicorn)
