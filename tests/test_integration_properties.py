import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_property():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/properties/", json={
            "title": "Casa de Férias Algarve",
            "address_street": "Av Github",
            "address_number": "2024",
            "address_neighborhood": "Jurerê",
            "address_city": "Florianópolis",
            "address_state": "SC",
            "country": "BRA",
            "rooms": 3,
            "capacity": 6,
            "price_per_night": 120.00
        })
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["title"] == "Casa de Férias Algarve"
    assert data["capacity"] == 6
