""" bancho.py's v2 apis for interacting with chat """

from __future__ import annotations

from fastapi import APIRouter
from fastapi import status
from fastapi.param_functions import Query

import app.state.sessions

from app.api.v2.common import responses
from app.api.v2.common.responses import Failure
from app.api.v2.common.responses import Success

from app.api.v2.models.players import Player
from app.api.v2.models.channels import Channel
from app.repositories import users as users_repo
from app.repositories import channels as channels_repo

router = APIRouter()

@router.get("/chat/channels")
async def chat_get_channels(
    read_priv: int | None = None,
    write_priv: int | None = None,
    auto_join: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
) -> Success[list[Channel]] | Failure:
    channels = await channels_repo.fetch_many(
        read_priv=read_priv,
        write_priv=write_priv,
        auto_join=auto_join,
        page=page,
        page_size=page_size,
    )
    total_channels = await channels_repo.fetch_count(
        read_priv=read_priv,
        write_priv=write_priv,
        auto_join=auto_join,
    )
    
    response = [Channel.from_mapping(rec) for rec in channels]
    
    return responses.success(
        content=response,
        meta={
            "total": total_channels,
            "page": page,
            "page_size": page_size,
        },
    )

@router.get("/chat/channels/{channel}")
async def chat_get_channel(
    channel: str
) -> Success[Channel] | Failure:
    channel_data = await channels_repo.fetch_one(name=''.join(('#', channel)))
    if channel_data is None:
        return responses.failure(
            message="Channel not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    response = Channel.from_mapping(channel_data)
    return responses.success(response)

@router.put("/chat/channels/{channel}/users/{user_id}")
async def chat_join(
    channel: str,
    user_id: int
) -> Success[Channel] | Failure:
    channel_data = await channels_repo.fetch_one(name=''.join(('#', channel)))
    user_data = await users_repo.fetch_one(id=user_id)
    
    if channel_data is None:
        return responses.failure(
            message="Channel not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        
    if user_data is None:
        return responses.failure(
            message="User not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    session_channel = app.state.sessions.channels.get_by_name(channel)
    session_player = app.state.sessions.players.get(id=user_id)
    session_channel.append(session_player)

    response = Channel.from_mapping(channel_data)
    return responses.success(response)