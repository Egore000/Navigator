from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 201),
    ("kot@pes.com", "k0t0pes", 409),
    ("email", "password", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", params={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("email", "password", 422),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", params={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
