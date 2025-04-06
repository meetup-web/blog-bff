from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from blog_bff.application.models.comment import CommentReadModel
from blog_bff.application.models.pagination import Pagination
from blog_bff.application.queries.load_post_comments import LoadPostComments
from blog_bff.infrastructure.query_bus.adapters.sender import Sender
from blog_bff.presentation.api.response_models import SuccessResponse

COMMENTS_ROUTER = APIRouter(prefix="/comments", tags=["Comments"])


@COMMENTS_ROUTER.get(
    "/post/{post_id}",
    responses={HTTP_200_OK: {"model": SuccessResponse[list[CommentReadModel]]}},
    status_code=HTTP_200_OK,
)
@inject
async def load_post_comments(
    post_id: UUID,
    pagination: Annotated[Pagination, Depends()],
    *,
    query_sender: FromDishka[Sender],
) -> SuccessResponse[list[CommentReadModel]]:
    comments = await query_sender.send(
        LoadPostComments(post_id=post_id, pagination=pagination)
    )
    return SuccessResponse(result=comments, status=HTTP_200_OK)
