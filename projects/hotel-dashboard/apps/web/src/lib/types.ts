export interface HotelSummary {
	hotel_id: string;
	hotel_name: string;
	total_revenue: number;
	adr: number;
	revpar: number;
	occupancy_rate: number;
	cancellation_rate: number;
	total_bookings: number;
}

export interface DashboardSummary {
	hotels: HotelSummary[];
	total_revenue: number;
	avg_adr: number;
	avg_occupancy_rate: number;
	avg_cancellation_rate: number;
}

export interface DailyTrend {
	date: string;
	revenue: number;
	bookings: number;
}

export interface TrendsResponse {
	hotel_id: string | null;
	trends: DailyTrend[];
}

export interface HotelDetail {
	hotel_id: string;
	hotel_name: string;
	pms_type: string;
	total_rooms: number;
	total_revenue: number;
	adr: number;
	revpar: number;
	occupancy_rate: number;
	cancellation_rate: number;
	total_bookings: number;
	trends: DailyTrend[];
}
