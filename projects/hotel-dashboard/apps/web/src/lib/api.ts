import type { DashboardSummary, HotelDetail, TrendsResponse } from "./types";

const API_BASE = "http://localhost:8000";

async function fetchJson<T>(url: string): Promise<T> {
	const res = await fetch(url);
	if (!res.ok) {
		throw new Error(`API error: ${res.status} ${res.statusText}`);
	}
	return res.json() as Promise<T>;
}

export function fetchDashboardSummary(): Promise<DashboardSummary> {
	return fetchJson<DashboardSummary>(`${API_BASE}/api/dashboard/summary`);
}

export function fetchTrends(
	hotelId?: string | null,
	days = 30,
): Promise<TrendsResponse> {
	const params = new URLSearchParams();
	if (hotelId) params.set("hotel_id", hotelId);
	params.set("days", String(days));
	return fetchJson<TrendsResponse>(
		`${API_BASE}/api/dashboard/trends?${params}`,
	);
}

export function fetchHotelDetail(hotelId: string): Promise<HotelDetail> {
	return fetchJson<HotelDetail>(
		`${API_BASE}/api/dashboard/hotel/${hotelId}`,
	);
}
