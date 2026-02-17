from app.core.config import HOTELS
from app.core.database import get_db
from app.models.schemas import (
    DailyTrend,
    DashboardSummary,
    HotelDetail,
    HotelSummary,
    TrendsResponse,
)


def get_hotel_config(hotel_id: str):
    """Look up hotel config by ID."""
    for hotel in HOTELS:
        if hotel.hotel_id == hotel_id:
            return hotel
    return None


def get_dashboard_summary() -> DashboardSummary:
    """Fetch aggregated summary metrics for all hotels."""
    db = get_db()

    result = db.execute("""
        SELECT
            hotel_id,
            SUM(revenue) as total_revenue,
            AVG(adr) as adr,
            AVG(revpar) as revpar,
            AVG(occupancy_rate) as occupancy_rate,
            AVG(cancellation_rate) as cancellation_rate,
            SUM(total_bookings) as total_bookings
        FROM gold_revenue_by_hotel
        GROUP BY hotel_id
    """).fetchall()

    hotels = []
    for row in result:
        config = get_hotel_config(row[0])
        hotels.append(
            HotelSummary(
                hotel_id=row[0],
                hotel_name=config.name if config else row[0],
                total_revenue=row[1] or 0,
                adr=row[2] or 0,
                revpar=row[3] or 0,
                occupancy_rate=row[4] or 0,
                cancellation_rate=row[5] or 0,
                total_bookings=row[6] or 0,
            )
        )

    total_revenue = sum(h.total_revenue for h in hotels)
    avg_adr = sum(h.adr for h in hotels) / len(hotels) if hotels else 0
    avg_occupancy = sum(h.occupancy_rate for h in hotels) / len(hotels) if hotels else 0
    avg_cancellation = sum(h.cancellation_rate for h in hotels) / len(hotels) if hotels else 0

    return DashboardSummary(
        hotels=hotels,
        total_revenue=total_revenue,
        avg_adr=avg_adr,
        avg_occupancy_rate=avg_occupancy,
        avg_cancellation_rate=avg_cancellation,
    )


def get_trends(hotel_id: str | None = None, days: int = 30) -> TrendsResponse:
    """Fetch daily revenue trends for the last N days."""
    db = get_db()

    if hotel_id:
        result = db.execute(
            """
            SELECT date, revenue, total_bookings
            FROM gold_revenue_by_hotel
            WHERE hotel_id = ?
            ORDER BY date DESC
            LIMIT ?
            """,
            [hotel_id, days],
        ).fetchall()
    else:
        result = db.execute(
            """
            SELECT date, SUM(revenue) as revenue, SUM(total_bookings) as total_bookings
            FROM gold_revenue_by_hotel
            GROUP BY date
            ORDER BY date DESC
            LIMIT ?
            """,
            [days],
        ).fetchall()

    trends = [
        DailyTrend(date=row[0], revenue=row[1] or 0, bookings=row[2] or 0)
        for row in result
    ]
    trends.reverse()

    return TrendsResponse(hotel_id=hotel_id, trends=trends)


def get_hotel_detail(hotel_id: str) -> HotelDetail | None:
    """Fetch detailed stats for a single hotel property."""
    config = get_hotel_config(hotel_id)
    if not config:
        return None

    db = get_db()

    summary = db.execute(
        """
        SELECT
            SUM(revenue) as total_revenue,
            AVG(adr) as adr,
            AVG(revpar) as revpar,
            AVG(occupancy_rate) as occupancy_rate,
            AVG(cancellation_rate) as cancellation_rate,
            SUM(total_bookings) as total_bookings
        FROM gold_revenue_by_hotel
        WHERE hotel_id = ?
        """,
        [hotel_id],
    ).fetchone()

    trends_data = db.execute(
        """
        SELECT date, revenue, total_bookings
        FROM gold_revenue_by_hotel
        WHERE hotel_id = ?
        ORDER BY date DESC
        LIMIT 30
        """,
        [hotel_id],
    ).fetchall()

    trends = [
        DailyTrend(date=row[0], revenue=row[1] or 0, bookings=row[2] or 0)
        for row in trends_data
    ]
    trends.reverse()

    return HotelDetail(
        hotel_id=hotel_id,
        hotel_name=config.name,
        pms_type=config.pms_type,
        total_rooms=config.total_rooms,
        total_revenue=summary[0] or 0 if summary else 0,
        adr=summary[1] or 0 if summary else 0,
        revpar=summary[2] or 0 if summary else 0,
        occupancy_rate=summary[3] or 0 if summary else 0,
        cancellation_rate=summary[4] or 0 if summary else 0,
        total_bookings=summary[5] or 0 if summary else 0,
        trends=trends,
    )
