from datetime import datetime, timedelta

import pytest

from pydantic import ValidationError

from app.schemas import (
    ReservationBase,
    ReservationCreate,
    ReservationDB,
    ReservationUpdate,
)

START = datetime.now() + timedelta(days=1)
END = START + timedelta(hours=1)
PAST = datetime.now() - timedelta(days=1)


def test_reservation_create_valid():
    obj = ReservationCreate(
        from_reserve=START,
        to_reserve=END,
        meetingroom_id=5,
    )

    assert obj.from_reserve == START
    assert obj.to_reserve == END
    assert obj.meetingroom_id == 5


def test_reservation_create_missing_meetingroom_id():
    with pytest.raises(ValidationError):
        ReservationCreate(
            from_reserve=START,
            to_reserve=END,
        )


def test_reservation_update_past_start():
    with pytest.raises(ValidationError):
        ReservationUpdate(
            from_reserve=PAST,
            to_reserve=PAST + timedelta(hours=1),
        )


def test_reservation_create_past_start():
    with pytest.raises(ValidationError):
        ReservationCreate(
            from_reserve=PAST,
            to_reserve=PAST + timedelta(hours=1),
            meetingroom_id=1,
        )


def test_reservation_start_after_end():
    with pytest.raises(ValidationError):
        ReservationUpdate(
            from_reserve=END,
            to_reserve=START,
        )


def test_reservation_start_equals_end():
    with pytest.raises(ValidationError):
        ReservationUpdate(
            from_reserve=START,
            to_reserve=START,
        )


def test_reservation_crosses_midnight_is_valid():
    day = (datetime.now() + timedelta(days=1)).date()

    start = datetime(day.year, day.month, day.day, 23, 0)
    end = start + timedelta(hours=2)

    obj = ReservationUpdate(
        from_reserve=start,
        to_reserve=end,
    )

    assert obj.to_reserve.day != obj.from_reserve.day


class _FakeDatetime:
    @classmethod
    def now(cls):
        return datetime(2026, 7, 1, 12, 0)


def test_reservation_start_equal_now_is_past(monkeypatch):
    monkeypatch.setattr(
        "app.schemas.reservation.datetime",
        _FakeDatetime,
    )

    with pytest.raises(ValidationError):
        ReservationUpdate(
            from_reserve=datetime(2026, 7, 1, 12, 0),
            to_reserve=datetime(2026, 7, 1, 13, 0),
        )


def test_reservation_base_accepts_past():
    obj = ReservationBase(
        from_reserve=PAST,
        to_reserve=PAST - timedelta(hours=1),
    )

    assert obj.from_reserve == PAST


def test_reservation_extra_field_forbidden():
    with pytest.raises(ValidationError):
        ReservationBase(
            from_reserve=START,
            to_reserve=END,
            unexpected="field",
        )

    with pytest.raises(ValidationError):
        ReservationCreate(
            from_reserve=START,
            to_reserve=END,
            meetingroom_id=1,
            unexpected="field",
        )


def test_reservation_db_from_attributes():
    class _Row:
        id = 7
        from_reserve = PAST
        to_reserve = PAST + timedelta(hours=1)
        meetingroom_id = 3
        user_id = None

    obj = ReservationDB.from_orm(_Row())

    assert obj.id == 7
    assert obj.meetingroom_id == 3
    assert obj.user_id is None
    assert obj.from_reserve == PAST
