import { HotelSelector } from "@/components/HotelSelector";
import { KPICard } from "@/components/KPICard";
import { TrendChart } from "@/components/TrendChart";
import { fetchDashboardSummary, fetchTrends } from "@/lib/api";
import type { DashboardSummary, TrendsResponse } from "@/lib/types";
import { Link, createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";

export const Route = createFileRoute("/")({ component: Dashboard });

const fmtCurrency = (n: number) =>
	`$${Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(n)}`;

const fmtPercent = (n: number) => `${(n * 100).toFixed(1)}%`;

function Dashboard() {
	const [summary, setSummary] = useState<DashboardSummary | null>(null);
	const [trends, setTrends] = useState<TrendsResponse | null>(null);
	const [selectedHotel, setSelectedHotel] = useState<string | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		fetchDashboardSummary()
			.then(setSummary)
			.catch((err) => setError(err.message))
			.finally(() => setLoading(false));
	}, []);

	useEffect(() => {
		fetchTrends(selectedHotel).then(setTrends).catch(console.error);
	}, [selectedHotel]);

	if (loading) {
		return (
			<div className="flex h-screen items-center justify-center">
				<p className="text-tremor-content dark:text-dark-tremor-content">
					Loading dashboard...
				</p>
			</div>
		);
	}

	if (error || !summary) {
		return (
			<div className="flex h-screen items-center justify-center">
				<div className="text-center">
					<p className="text-red-600 dark:text-red-400">
						{error ?? "Failed to load data"}
					</p>
					<p className="mt-2 text-tremor-default text-tremor-content dark:text-dark-tremor-content">
						Make sure the backend is running at http://localhost:8000
					</p>
				</div>
			</div>
		);
	}

	return (
		<div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
			{/* Header */}
			<div className="mb-8 flex items-center justify-between">
				<div>
					<h1 className="text-tremor-title font-bold text-tremor-content-strong dark:text-dark-tremor-content-strong text-2xl">
						Hotel Dashboard
							</h1>
					<p className="mt-1 text-tremor-default text-tremor-content dark:text-dark-tremor-content">
						Real-time performance metrics across {summary.hotels.length}{" "}
						properties
					</p>
				</div>
				<div className="w-64">
					<HotelSelector
						hotels={summary.hotels}
						selected={selectedHotel}
						onSelect={setSelectedHotel}
					/>
				</div>
			</div>

			{/* KPI Cards */}
			<dl className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
				<KPICard
					title="Total Revenue"
					value={fmtCurrency(summary.total_revenue)}
				/>
				<KPICard
					title="Avg. Daily Rate (ADR)"
					value={fmtCurrency(summary.avg_adr)}
				/>
				<KPICard
					title="Avg. Occupancy Rate"
					value={fmtPercent(summary.avg_occupancy_rate)}
				/>
				<KPICard
					title="Avg. Cancellation Rate"
					value={fmtPercent(summary.avg_cancellation_rate)}
					trend={summary.avg_cancellation_rate > 0.2 ? "negative" : "positive"}
				/>
			</dl>

			{/* Trend Chart */}
			{trends && (
				<div className="mb-8">
					<TrendChart
						title="Revenue Trend"
						subtitle={`Daily revenue — last 30 days${selectedHotel ? ` (${summary.hotels.find((h) => h.hotel_id === selectedHotel)?.hotel_name})` : ""}`}
						data={trends.trends}
					/>
				</div>
			)}

			{/* Hotel Breakdown */}
			<h2 className="mb-4 text-tremor-title font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
				Properties
			</h2>
			<div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
				{summary.hotels.map((hotel) => (
					<Link
						key={hotel.hotel_id}
						to="/hotel/$hotelId"
						params={{ hotelId: hotel.hotel_id }}
						className="block"
					>
						<div className="rounded-tremor-default border border-tremor-border p-6 transition-shadow hover:shadow-tremor-card dark:border-dark-tremor-border dark:hover:shadow-dark-tremor-card">
							<h3 className="text-tremor-default font-medium text-tremor-content-strong dark:text-dark-tremor-content-strong">
								{hotel.hotel_name}
							</h3>
							<div className="mt-4 grid grid-cols-2 gap-4">
								<div>
									<p className="text-tremor-label text-tremor-content dark:text-dark-tremor-content">
										Revenue
									</p>
									<p className="text-tremor-default font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
										{fmtCurrency(hotel.total_revenue)}
									</p>
								</div>
								<div>
									<p className="text-tremor-label text-tremor-content dark:text-dark-tremor-content">
										ADR
									</p>
									<p className="text-tremor-default font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
										{fmtCurrency(hotel.adr)}
									</p>
								</div>
								<div>
									<p className="text-tremor-label text-tremor-content dark:text-dark-tremor-content">
										Occupancy
									</p>
									<p className="text-tremor-default font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
										{fmtPercent(hotel.occupancy_rate)}
									</p>
								</div>
								<div>
									<p className="text-tremor-label text-tremor-content dark:text-dark-tremor-content">
										Bookings
									</p>
									<p className="text-tremor-default font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
										{hotel.total_bookings.toLocaleString()}
									</p>
								</div>
							</div>
						</div>
					</Link>
				))}
			</div>
		</div>
	);
}
