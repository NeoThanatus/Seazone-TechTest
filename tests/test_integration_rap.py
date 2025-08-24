import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_properties_and_reservations():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        # Mano Brown
        prop_mb = {
            "title": "Casa do Capão",
            "address_street": "Rua dos Racionais",
            "address_number": "1",
            "address_neighborhood": "Capão Redondo",
            "address_city": "São Paulo",
            "address_state": "SP",
            "country": "BRA",
            "rooms": 4,
            "capacity": 8,
            "price_per_night": 350.00
        }
        resp_mb = await ac.post("/properties/", json=prop_mb)
        assert resp_mb.status_code in [200, 201]
        id_mb = resp_mb.json()["property_id"]

        # Emicida
        prop_emc = {
            "title": "Estúdio Lab",
            "address_street": "Rua AmarElo",
            "address_number": "42",
            "address_neighborhood": "Barra Funda",
            "address_city": "São Paulo",
            "address_state": "SP",
            "country": "BRA",
            "rooms": 2,
            "capacity": 4,
            "price_per_night": 200.00
        }
        resp_emc = await ac.post("/properties/", json=prop_emc)
        assert resp_emc.status_code in [200, 201]
        id_emc = resp_emc.json()["property_id"]

        # BK
        prop_bk = {
            "title": "Cobertura do BK",
            "address_street": "Rua Líder",
            "address_number": "7",
            "address_neighborhood": "Lapa",
            "address_city": "Rio de Janeiro",
            "address_state": "RJ",
            "country": "BRA",
            "rooms": 3,
            "capacity": 6,
            "price_per_night": 300.00
        }
        resp_bk = await ac.post("/properties/", json=prop_bk)
        assert resp_bk.status_code in [200, 201]
        id_bk = resp_bk.json()["property_id"]

        # Baco
        prop_baco = {
            "title": "Casa do Blues",
            "address_street": "Rua Pelourinho",
            "address_number": "100",
            "address_neighborhood": "Pelourinho",
            "address_city": "Salvador",
            "address_state": "BA",
            "country": "BRA",
            "rooms": 2,
            "capacity": 5,
            "price_per_night": 220.00
        }
        resp_baco = await ac.post("/properties/", json=prop_baco)
        assert resp_baco.status_code in [200, 201]
        id_baco = resp_baco.json()["property_id"]

        # Reserva Emicida na Casa do Capão
        reserva_emc = {
            "property_id": id_mb,
            "client_name": "Emicida",
            "client_email": "emicida@lab.com",
            "start_date": "2024-12-10",
            "end_date": "2024-12-15",
            "guests_quantity": 4
        }
        resp_reserva_emc = await ac.post("/reservations/", json=reserva_emc)
        assert resp_reserva_emc.status_code in [200, 201]
        reserva_id_emc = resp_reserva_emc.json()["reservation_id"]

        # Reserva BK na Cobertura do BK
        reserva_bk = {
            "property_id": id_bk,
            "client_name": "BK",
            "client_email": "bk@lider.com",
            "start_date": "2024-12-20",
            "end_date": "2024-12-25",
            "guests_quantity": 3
        }
        resp_reserva_bk = await ac.post("/reservations/", json=reserva_bk)
        assert resp_reserva_bk.status_code in [200, 201]
        reserva_id_bk = resp_reserva_bk.json()["reservation_id"]

        # Reserva Baco na Casa do Blues (erro: excede capacidade)
        reserva_baco = {
            "property_id": id_baco,
            "client_name": "Baco Exu do Blues",
            "client_email": "baco@blues.com",
            "start_date": "2024-12-10",
            "end_date": "2024-12-15",
            "guests_quantity": 10
        }
        resp_reserva_baco = await ac.post("/reservations/", json=reserva_baco)
        assert resp_reserva_baco.status_code == 400
        assert resp_reserva_baco.json()["detail"] == "Guests exceed capacity"

        # Reserva Mano Brown na Casa do Capão (erro: sobreposição)
        reserva_mb = {
            "property_id": id_mb,
            "client_name": "Mano Brown",
            "client_email": "brown@racionais.com",
            "start_date": "2024-12-12",
            "end_date": "2024-12-18",
            "guests_quantity": 2
        }
        resp_reserva_mb = await ac.post("/reservations/", json=reserva_mb)
        assert resp_reserva_mb.status_code == 400
        assert resp_reserva_mb.json()["detail"] == "Property not available for these dates"
