from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import DashboardSummary, HotelDetail, TrendsResponse
from app.services.dashboard_service import (
    get_dashboard_summary,
    get_hotel_detail,
    get_trends,
)

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary():
    """Returns total revenue, ADR, bookings for all hotels."""
    return get_dashboard_summary()


@router.get("/trends", response_model=TrendsResponse)
async def dashboard_trends(
    hotel_id: str | None = Query(None, description="Filter by hotel ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days"),
):
    """Returns daily revenue trend for the last N days."""
    return get_trends(hotel_id=hotel_id, days=days)


@router.get("/hotel/{hotel_id}", response_model=HotelDetail)
async def hotel_detail(hotel_id: str):
    """Returns specific stats for one hotel property."""
    detail = get_hotel_detail(hotel_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Hotel '{hotel_id}' not found")
    return detail
