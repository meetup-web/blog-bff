from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from blog_bff.application.models.pagination import Pagination
from blog_bff.application.models.post import PostReadModel
from blog_bff.application.queries.load_posts import LoadPosts
from blog_bff.application.queries.load_user_posts import LoadUserPosts
from blog_bff.infrastructure.query_bus.adapters.sender import Sender
from blog_bff.presentation.api.response_models import SuccessResponse

POSTS_ROUTER = APIRouter(prefix="/posts", tags=["posts"])


@POSTS_ROUTER.get(
    path="/",
    responses={HTTP_200_OK: {"model": SuccessResponse[list[PostReadModel]]}},
    status_code=HTTP_200_OK,
)
@inject
async def load_posts(
    pagination: Annotated[Pagination, Depends()], *, query_sender: FromDishka[Sender]
) -> SuccessResponse[list[PostReadModel]]:
    posts = await query_sender.send(LoadPosts(pagination=pagination))
    return SuccessResponse(result=posts, status=HTTP_200_OK)


@POSTS_ROUTER.get(
    path="/{user_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[list[PostReadModel]]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def load_user_posts(
    user_id: UUID,
    pagination: Annotated[Pagination, Depends()],
    *,
    query_sender: FromDishka[Sender],
) -> SuccessResponse[list[PostReadModel]]:
    posts = await query_sender.send(LoadUserPosts(user_id=user_id, pagination=pagination))
    return SuccessResponse(result=posts, status=HTTP_200_OK)
