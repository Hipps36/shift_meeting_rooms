from datetime import date, datetime, time, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from pydantic import ValidationError

from app.crud import reservation_crud
from app.schemas import (
    MeetingRoomCreate,
    MeetingRoomDB,
    MeetingRoomUpdate,
)


def test_create_valid_with_name_and_description():
    room = MeetingRoomCreate(name='Переговорка A', description='у окна')
    assert room.name == 'Переговорка A'
    assert room.description == 'у окна'


def test_create_description_none_allowed():
    room = MeetingRoomCreate(name='A', description=None)
    assert room.name == 'A'
    assert room.description is None


def test_create_empty_name_raises():
    with pytest.raises(ValidationError):
        MeetingRoomCreate(name='', description=None)


def test_create_name_too_long_raises():
    with pytest.raises(ValidationError):
        MeetingRoomCreate(name='a' * 101, description=None)


def test_update_explicit_name_none_raises_custom_message():
    with pytest.raises(ValidationError) as exc_info:
        MeetingRoomUpdate(name=None, description='desc')
    assert 'Имя переговорной комнаты не может быть пустым.' in str(
        exc_info.value
    )


def test_update_name_omitted_defaults_to_none_ok():
    room = MeetingRoomUpdate(description='desc')
    assert room.name is None
    assert room.description == 'desc'


def test_db_from_attributes():
    class _Row:
        id = 7
        name = 'Room 7'
        description = 'угловая'
    room = MeetingRoomDB.from_orm(_Row())
    assert room.id == 7
    assert room.name == 'Room 7'
    assert room.description == 'угловая'


@pytest.mark.asyncio
async def test_get_future_available_for_room_one_reservation():
    test_date = date(2026, 7, 2)
    reservation = MagicMock()
    reservation.from_reserve = datetime.combine(test_date, time(10, 0))
    reservation.to_reserve = datetime.combine(test_date, time(12, 0))
    result = MagicMock()
    result.scalars.return_value.all.return_value = [reservation]
    session = AsyncMock()
    session.execute.return_value = result
    slots = await reservation_crud.get_future_available_for_room(
        room_id=1,
        date=test_date,
        session=session,
    )
    assert len(slots) == 2
    assert slots[0].start == datetime.combine(test_date, time.min)
    assert slots[0].end == datetime.combine(test_date, time(10, 0))
    assert slots[1].start == datetime.combine(test_date, time(12, 0))
    assert slots[1].end == datetime.combine(
        test_date + timedelta(days=1), time.min
    )


@pytest.mark.asyncio
async def test_get_future_available_for_room_no_reservations():
    test_date = date(2026, 7, 2)
    result = MagicMock()
    result.scalars.return_value.all.return_value = []
    session = AsyncMock()
    session.execute.return_value = result
    slots = await reservation_crud.get_future_available_for_room(
        room_id=1,
        date=test_date,
        session=session,
    )
    assert len(slots) == 1
    assert slots[0].start == datetime.combine(test_date, time.min)
    assert slots[0].end == datetime.combine(
        test_date + timedelta(days=1), time.min
    )
