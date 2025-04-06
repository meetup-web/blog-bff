from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from posts_bff.application.common.application_error import ApplicationError
from posts_bff.application.models.pagination import Pagination
from posts_bff.application.models.post import PostReadModel
from posts_bff.application.queries.load_post_by_id import LoadPostById
from posts_bff.application.queries.load_posts import LoadPosts
from posts_bff.infrastructure.query_bus.adapters.sender import Sender
from posts_bff.presentation.api.response_models import ErrorResponse, SuccessResponse

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
    path="/{post_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[PostReadModel]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def load_post_by_id(
    post_id: UUID, *, query_sender: FromDishka[Sender]
) -> SuccessResponse[PostReadModel]:
    post = await query_sender.send(LoadPostById(post_id=post_id))
    return SuccessResponse(result=post, status=HTTP_200_OK)
