from datetime import datetime

import pytest

from app.backend.bookings.service import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.insert(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.get_one_or_none(id=new_booking.id)

    assert new_booking


@pytest.mark.parametrize("user_id, room_id, date_from, date_to, price, total_cost, total_days",
    [
        (1, 1, "2024-06-11", "2024-06-14", 24500, 73500, 3),
        (2, 4, None, "2024-06-15", 4350, 21750, 5),
        (2, 4, "2024-06-12", None, 4350, 52200, 12),
        (2, 4, "2024-01-02", "2024-01-01", 4350, -4350, -1),
    ]
)
async def test_add_and_update_booking(
        user_id,
        room_id,
        date_from,
        date_to,
        price,
        total_cost,
        total_days
):
    new_booking = await BookingDAO.insert(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2024-06-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-06-24", "%Y-%m-%d"),
    )

    kwargs = {
        "user_id": user_id,
        "room_id": room_id,
    }
    if date_from is not None:
        kwargs.update({
            "date_from": datetime.strptime(date_from, "%Y-%m-%d")
        })
    if date_to is not None:
        kwargs.update({
            "date_to": datetime.strptime(date_to, "%Y-%m-%d")
        })

    updated_booking = await BookingDAO.update(
        new_booking.id,
        **kwargs,
    )

    assert updated_booking.user_id == user_id
    assert updated_booking.room_id == room_id

    if date_from is None:
        assert updated_booking.date_from == new_booking.date_from
    else:
        assert updated_booking.date_from == datetime.strptime(date_from, "%Y-%m-%d").date()

    if date_to is None:
        assert updated_booking.date_to == new_booking.date_to
    else:
        assert updated_booking.date_to == datetime.strptime(date_to, "%Y-%m-%d").date()

    assert updated_booking.price == price
    assert updated_booking.total_cost == total_cost
    assert updated_booking.total_days == total_days
