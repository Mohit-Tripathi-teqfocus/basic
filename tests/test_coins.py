from fastapi.testclient import TestClient
from app.main import app
import pytest
import respx
from httpx import Response
from fastapi import HTTPException
from app.services.coingecko import get_all_coins

client = TestClient(app)


def test_list_coins():
    """Test if /coins endpoint returns a valid list of coins."""
    response = client.get("/api/coins")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_categories():
    """Test if /categories endpoint returns a valid list of categories."""
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtered_coins_by_ids():
    """Test filtering coins using a specific coin ID."""
    response = client.get("/api/filtered-coins?ids=bitcoin")
    print("\nRESPONSE JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("id" in coin for coin in data)


def test_filtered_coins_by_category():
    """Test filtering coins using a specific category."""
    response = client.get("/api/filtered-coins?category=stablecoins")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtered_coins_pagination():
    """Test pagination on filtered coins endpoint."""
    response = client.get("/api/filtered-coins?page_num=1&per_page=5")
    print("\nPAGINATED RESPONSE:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("id" in coin for coin in data)


@pytest.mark.asyncio
@respx.mock
async def test_get_all_coins_function():
    """Test get_all_coins service function directly using mocked success and error responses."""
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # Success scenario
    mock_data = [{"id": "bitcoin"}, {"id": "ethereum"}]
    respx.get(url).mock(return_value=Response(200, json=mock_data))
    data = await get_all_coins(1, 2)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "bitcoin"

    # HTTPStatusError scenario
    respx.get(url).mock(return_value=Response(429, json={"error": "Too many requests"}))
    with pytest.raises(HTTPException) as exc_info:
        await get_all_coins(1, 2)
    assert exc_info.value.status_code == 429

    # Generic error scenario
    respx.get(url).mock(side_effect=Exception("Simulated failure"))
    with pytest.raises(HTTPException) as exc_info:
        await get_all_coins(1, 2)
    assert exc_info.value.status_code == 500
    assert "Unexpected error" in str(exc_info.value.detail)


def test_health_check():
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_info():
    """Test the /version endpoint."""
    response = client.get("/version")
    assert response.status_code == 200
    assert "app_version" in response.json()
    assert "coingecko_api" in response.json()
