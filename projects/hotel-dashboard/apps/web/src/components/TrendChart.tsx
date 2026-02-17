import type { DailyTrend } from "@/lib/types";
import { AreaChart, Card } from "@tremor/react";

interface TrendChartProps {
	title: string;
	subtitle?: string;
	data: DailyTrend[];
}

const currencyFormatter = (value: number) =>
	`$${Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 }).format(value)}`;

export function TrendChart({ title, subtitle, data }: TrendChartProps) {
	return (
		<Card>
			<h3 className="text-tremor-title font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
				{title}
			</h3>
			{subtitle && (
				<p className="mt-1 text-tremor-default text-tremor-content dark:text-dark-tremor-content">
					{subtitle}
				</p>
			)}
			<AreaChart
				className="mt-4 h-72"
				data={data}
				index="date"
				categories={["revenue"]}
				colors={["blue"]}
				valueFormatter={currencyFormatter}
				showLegend={false}
				showGradient={true}
				curveType="monotone"
			/>
		</Card>
	);
}
