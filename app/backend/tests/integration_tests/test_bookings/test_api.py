import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (4, "2030-05-01", "2030-05-10", 3, 200),
    (4, "2030-05-01", "2030-05-10", 4, 200),
    (4, "2030-05-01", "2030-05-10", 5, 200),
    (4, "2030-05-01", "2030-05-10", 6, 200),
    (4, "2030-05-01", "2030-05-10", 7, 200),
    (4, "2030-05-01", "2030-05-10", 8, 200),
    (4, "2030-05-01", "2030-05-10", 9, 200),
    (4, "2030-05-01", "2030-05-10", 10, 200),
    (4, "2030-05-01", "2030-05-10", 10, 409),
    (4, "2030-05-01", "2030-05-10", 10, 409),
])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        booked_rooms,
        status_code,
        authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms


@pytest.mark.parametrize("booking_id, booked_rooms_left, status_code", [
    (10, 9, 200),
    (10, 9, 404),
    (8, 8, 200),
    (34, 8, 404),
    (3, 8, 404),
])
async def test_delete_and_get_bookings(
        booking_id,
        booked_rooms_left,
        status_code,
        authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.delete(f"/bookings/{booking_id}")
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms_left


@pytest.mark.parametrize("booking_id, room_id, date_from, date_to, price, status_code", [
    (4, None, None, None, 4350, 200),
    (5, 4, "2023-05-20", "2023-05-25", 4350, 200),
    (1, 7, None, "2023-06-26", 4300, 200),
    (45, 3, "2024-06-10", "2024-06-15", 4570, 403),
    (1, 7, "2030-05-20", "2020-05-20", 4300, 400),
    (5, 4, "2024-05-25", None, 4350, 400),
    (5, 4, None, "2021-05-20", 4350, 400),
])
async def test_update_and_get_bookings(
        booking_id,
        room_id,
        date_from,
        date_to,
        price,
        status_code,
        authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(f"/bookings/{booking_id}")

    initial = response.json()

    params = {}
    if room_id is not None:
        params.update({"room_id": room_id})
    if date_from is not None:
        params.update({"date_from": date_from})
    if date_to is not None:
        params.update({"date_to": date_to})

    new_response = await authenticated_ac.patch(f"/bookings/{booking_id}", params=params)
    assert new_response.status_code == status_code

    updated = new_response.json()

    if new_response.status_code == 200:
        if room_id is not None:
            assert updated["room_id"] == room_id
        else:
            assert updated["room_id"] == initial["room_id"]

        if date_from is not None:
            assert updated["date_from"] == date_from
        else:
            assert updated["date_from"] == initial["date_from"]

        if date_to is not None:
            assert updated["date_to"] == date_to
        else:
            assert updated["date_to"] == initial["date_to"]

        assert updated["price"] == price
        assert updated["user_id"] == 1
