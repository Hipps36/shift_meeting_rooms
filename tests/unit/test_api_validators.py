from unittest.mock import AsyncMock

import pytest

from fastapi import HTTPException

from app.api.validators import (
    check_name_duplicate, check_meeting_room_exists,
    check_reservation_intersections, check_reservation_before_edit
)


@pytest.mark.asyncio
async def test_check_name_duplicate_raises(monkeypatch):

    mock_get_id = AsyncMock(return_value=1)

    monkeypatch.setattr(
        'app.crud.meeting_room.meeting_room_crud.get_room_id_by_name',
        mock_get_id
    )

    with pytest.raises(HTTPException) as exc:
        await check_name_duplicate('Room 1', AsyncMock())

    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_check_name_duplicate_ok(monkeypatch):

    mock_get_id = AsyncMock(return_value=None)

    monkeypatch.setattr(
        'app.crud.meeting_room.meeting_room_crud.get_room_id_by_name',
        mock_get_id
    )

    result = await check_name_duplicate('Room 1', AsyncMock())

    assert result is None


@pytest.mark.asyncio
async def test_room_exists(monkeypatch):

    mock_room = {'id': 1, 'name': 'Room'}

    monkeypatch.setattr(
        'app.crud.meeting_room.meeting_room_crud.get',
        AsyncMock(return_value=mock_room)
    )

    result = await check_meeting_room_exists(1, AsyncMock())

    assert result == mock_room


@pytest.mark.asyncio
async def test_room_not_found(monkeypatch):

    monkeypatch.setattr(
        'app.crud.meeting_room.meeting_room_crud.get',
        AsyncMock(return_value=None)
    )

    with pytest.raises(HTTPException) as exc:
        await check_meeting_room_exists(999, AsyncMock())

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_reservation_intersection(monkeypatch):

    monkeypatch.setattr(
        'app.crud.reservation.reservation_crud'
        '.get_reservations_at_the_same_time',
        AsyncMock(return_value=[{'id': 1}])
    )

    with pytest.raises(HTTPException) as exc:
        await check_reservation_intersections(room_id=1)

    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_reservation_no_intersection(monkeypatch):

    monkeypatch.setattr(
        'app.crud.reservation.reservation_crud.'
        'get_reservations_at_the_same_time',
        AsyncMock(return_value=[])
    )

    result = await check_reservation_intersections(room_id=1)

    assert result is None


@pytest.mark.asyncio
async def test_reservation_not_found(monkeypatch):

    monkeypatch.setattr(
        'app.crud.reservation.reservation_crud.get',
        AsyncMock(return_value=None)
    )

    user = type('User', (), {'id': 1, 'is_superuser': False})

    with pytest.raises(HTTPException) as exc:
        await check_reservation_before_edit(1, AsyncMock(), user)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_reservation_forbidden(monkeypatch):

    reservation = type('R', (), {'user_id': 2})

    monkeypatch.setattr(
        'app.crud.reservation.reservation_crud.get',
        AsyncMock(return_value=reservation)
    )

    user = type('User', (), {'id': 1, 'is_superuser': False})

    with pytest.raises(HTTPException) as exc:
        await check_reservation_before_edit(1, AsyncMock(), user)

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_reservation_ok(monkeypatch):

    reservation = type('R', (), {'user_id': 1})

    monkeypatch.setattr(
        'app.crud.reservation.reservation_crud.get',
        AsyncMock(return_value=reservation)
    )

    user = type('User', (), {'id': 1, 'is_superuser': False})

    result = await check_reservation_before_edit(1, AsyncMock(), user)

    assert result == reservation
