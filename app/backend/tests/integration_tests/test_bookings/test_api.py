from httpx import AsyncClient
import pytest


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

