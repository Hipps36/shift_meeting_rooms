from datetime import date, datetime, time, timedelta
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Reservation, User
from app.schemas.reservation import (
    ReservationCreate, ReservationUpdate, TimeSlot
)


class CRUDReservation(CRUDBase[
    Reservation, ReservationCreate, ReservationUpdate
]):

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve < Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.scalars(select_stmt)
        reservations = reservations.all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_available_for_room(
            self,
            room_id: int,
            date: date,
            session: AsyncSession,
    ):
        start = datetime.combine(date, time.min)
        end = start + timedelta(days=1)

        reservations = await session.execute(
            select(Reservation)
            .where(
                Reservation.meetingroom_id == room_id,
                Reservation.from_reserve < end,
                Reservation.to_reserve > start,
            )
            .order_by(Reservation.from_reserve)
        )
        reservations = reservations.scalars().all()

        available = []
        current = start

        for reservation in reservations:
            if reservation.from_reserve > current:
                available.append(
                    TimeSlot(start=current, end=reservation.from_reserve)
                )
            if reservation.to_reserve > current:
                current = reservation.to_reserve

        if current < end:
            available.append(
                TimeSlot(start=current, end=end)
            )

        return available

    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        return reservations.scalars().all()


reservation_crud = CRUDReservation(Reservation)
