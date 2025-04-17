import httpx
from fastapi import HTTPException
from typing import Dict, Any, List
import os

API_BASE = os.getenv("COINGECKO_API_BASE", "https://api.coingecko.com/api/v3")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "cad")


async def fetch_from_coingecko(
    endpoint: str, params: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Helper function to send a GET request to a CoinGecko endpoint with error handling.

    Args:
        endpoint (str): The specific API path.
        params (Dict[str, Any]): Query parameters.

    Returns:
        List[Dict[str, Any]]: JSON response from CoinGecko.
    """
    url = f"{API_BASE}{endpoint}"
    params = {k: v for k, v in params.items() if v is not None}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


async def get_all_coins(page: int, per_page: int) -> List[Dict[str, Any]]:
    """Get a list of coins with pagination sorted by market cap."""
    return await fetch_from_coingecko(
        "/coins/markets",
        {
            "vs_currency": DEFAULT_CURRENCY,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
        },
    )


async def get_categories() -> List[Dict[str, Any]]:
    """Retrieve the full list of available coin categories."""
    return await fetch_from_coingecko("/coins/categories/list", {})


async def get_coins_by_filter(
    ids: str, category: str, page: int, per_page: int
) -> List[Dict[str, Any]]:
    """
    Filter coins based on provided IDs and/or category with pagination.

    Args:
        ids (str): Comma-separated coin IDs.
        category (str): Coin category.
        page (int): Page number.
        per_page (int): Items per page.

    Returns:
        List[Dict[str, Any]]: Filtered list of coins.
    """
    cleaned_ids = ",".join(
        [coin_id.strip() for coin_id in ids.split(",") if coin_id.strip()]
    )
    return await fetch_from_coingecko(
        "/coins/markets",
        {
            "vs_currency": DEFAULT_CURRENCY,
            "ids": cleaned_ids if cleaned_ids else None,
            "category": category if category else None,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
        },
    )
