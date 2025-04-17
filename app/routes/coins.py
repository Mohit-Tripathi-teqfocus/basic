from fastapi import APIRouter, Query
from app.services.coingecko import get_all_coins, get_categories, get_coins_by_filter
from typing import List

router = APIRouter()


@router.get("/coins")
async def list_coins(page_num: int = 1, per_page: int = 10) -> List[dict]:
    """Fetches a paginated list of coins from the CoinGecko API."""
    return await get_all_coins(page_num, per_page)


@router.get("/categories")
async def list_categories() -> List[dict]:
    """Retrieves all available coin categories from CoinGecko."""
    return await get_categories()


@router.get("/filtered-coins")
async def list_filtered_coins(
    ids: str = "", category: str = "", page_num: int = 1, per_page: int = 10
) -> List[dict]:
    """Fetches filtered coin data based on IDs and/or category with pagination."""
    return await get_coins_by_filter(ids, category, page_num, per_page)
