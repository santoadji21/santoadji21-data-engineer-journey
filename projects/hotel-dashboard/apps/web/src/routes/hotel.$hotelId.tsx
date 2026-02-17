import { KPICard } from "@/components/KPICard";
import { TrendChart } from "@/components/TrendChart";
import { fetchHotelDetail } from "@/lib/api";
import type { HotelDetail } from "@/lib/types";
import { Link, createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { RiArrowLeftLine } from "@remixicon/react";
import { Badge } from "@tremor/react";

export const Route = createFileRoute("/hotel/$hotelId")({
	component: HotelDetailPage,
});

const fmtCurrency = (n: number) =>
	`$${Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(n)}`;

const fmtPercent = (n: number) => `${(n * 100).toFixed(1)}%`;

const pmsColors: Record<string, string> = {
	legacy: "amber",
	modern: "blue",
	budget: "emerald",
};

function HotelDetailPage() {
	const { hotelId } = Route.useParams();
	const [detail, setDetail] = useState<HotelDetail | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		setLoading(true);
		fetchHotelDetail(hotelId)
			.then(setDetail)
			.catch((err) => setError(err.message))
			.finally(() => setLoading(false));
	}, [hotelId]);

	if (loading) {
		return (
			<div className="flex h-screen items-center justify-center">
				<p className="text-tremor-content dark:text-dark-tremor-content">
					Loading hotel data...
				</p>
			</div>
		);
	}

	if (error || !detail) {
		return (
			<div className="flex h-screen items-center justify-center">
				<div className="text-center">
					<p className="text-red-600 dark:text-red-400">
						{error ?? "Hotel not found"}
					</p>
					<Link
						to="/"
						className="mt-4 inline-block text-tremor-brand underline"
					>
						Back to dashboard
					</Link>
				</div>
			</div>
		);
	}

	return (
		<div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
			{/* Header */}
			<div className="mb-8">
				<Link
					to="/"
					className="mb-4 inline-flex items-center gap-1 text-tremor-default text-tremor-brand hover:underline"
				>
					<RiArrowLeftLine className="size-4" />
					Back to dashboard
				</Link>
				<div className="flex items-center gap-3">
					<h1 className="text-2xl font-bold text-tremor-content-strong dark:text-dark-tremor-content-strong">
						{detail.hotel_name}
					</h1>
					<Badge color={pmsColors[detail.pms_type] ?? "gray"}>
						{detail.pms_type.toUpperCase()} PMS
					</Badge>
				</div>
				<p className="mt-1 text-tremor-default text-tremor-content dark:text-dark-tremor-content">
					{detail.total_rooms} rooms
				</p>
			</div>

			{/* KPI Cards */}
			<dl className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
				<KPICard
					title="Total Revenue"
					value={fmtCurrency(detail.total_revenue)}
				/>
				<KPICard
					title="ADR (Avg Daily Rate)"
					value={fmtCurrency(detail.adr)}
				/>
				<KPICard
					title="RevPAR"
					value={fmtCurrency(detail.revpar)}
					subtitle="Revenue per available room"
				/>
				<KPICard
					title="Occupancy Rate"
					value={fmtPercent(detail.occupancy_rate)}
					trend={detail.occupancy_rate > 0.7 ? "positive" : "negative"}
					subtitle={`${detail.total_rooms} total rooms`}
				/>
			</dl>

			{/* More metrics */}
			<dl className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-3">
				<KPICard
					title="Total Bookings"
					value={detail.total_bookings.toLocaleString()}
				/>
				<KPICard
					title="Cancellation Rate"
					value={fmtPercent(detail.cancellation_rate)}
					trend={detail.cancellation_rate > 0.2 ? "negative" : "positive"}
				/>
				<KPICard
					title="PMS Type"
					value={detail.pms_type.charAt(0).toUpperCase() + detail.pms_type.slice(1)}
				/>
			</dl>

			{/* Trend Chart */}
			<TrendChart
				title="Revenue Trend"
				subtitle="Daily revenue — last 30 days"
				data={detail.trends}
			/>
		</div>
	);
}
