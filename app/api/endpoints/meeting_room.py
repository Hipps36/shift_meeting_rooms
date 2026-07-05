from datetime import date

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import meeting_room_crud, reservation_crud
from app.schemas import (
    MeetingRoomCreate, MeetingRoomUpdate, MeetingRoomDB,
    ReservationDB, TimeSlot
)


router = APIRouter()


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Создание переговорной комнаты.

    Только для суперюзеров.
    """
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получение всех переговорных комнат.

    Только для авторизованных пользователей.
    """
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Чатичное обновление переговорной комнаты.

    Только для суперюзеров.
    """
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление переговорной комнаты.

    Только для суперюзеров.
    """
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
    dependencies=[Depends(current_superuser)],
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получение бронированей для переговорной комнаты.

    Только для суперюзеров.
    """
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservations


@router.get(
    '/{meeting_room_id}/available',
    response_model=list[TimeSlot],
    dependencies=[Depends(current_user)],
)
async def get_available_for_room(
        meeting_room_id: int,
        date: date,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получние всех свободных временных отрезков переговорной комнаты на
    определенную дату.

    Только для авторизованных пользователей.
    """
    await check_meeting_room_exists(meeting_room_id, session)
    available = await reservation_crud.get_future_available_for_room(
        room_id=meeting_room_id, date=date, session=session
    )
    return available
