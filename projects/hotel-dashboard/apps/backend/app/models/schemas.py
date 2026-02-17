from datetime import date

from pydantic import BaseModel


class HotelSummary(BaseModel):
    hotel_id: str
    hotel_name: str
    total_revenue: float
    adr: float  # Average Daily Rate
    revpar: float  # Revenue Per Available Room
    occupancy_rate: float
    cancellation_rate: float
    total_bookings: int


class DashboardSummary(BaseModel):
    hotels: list[HotelSummary]
    total_revenue: float
    avg_adr: float
    avg_occupancy_rate: float
    avg_cancellation_rate: float


class DailyTrend(BaseModel):
    date: date
    revenue: float
    bookings: int


class TrendsResponse(BaseModel):
    hotel_id: str | None
    trends: list[DailyTrend]


class HotelDetail(BaseModel):
    hotel_id: str
    hotel_name: str
    pms_type: str
    total_rooms: int
    total_revenue: float
    adr: float
    revpar: float
    occupancy_rate: float
    cancellation_rate: float
    total_bookings: int
    trends: list[DailyTrend]
