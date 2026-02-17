import { cn } from "@/lib/cn";
import { Card } from "@tremor/react";

interface KPICardProps {
	title: string;
	value: string;
	subtitle?: string;
	trend?: "positive" | "negative" | "neutral";
}

export function KPICard({ title, value, subtitle, trend }: KPICardProps) {
	return (
		<Card>
			<dt className="text-tremor-default font-medium text-tremor-content dark:text-dark-tremor-content">
				{title}
			</dt>
			<dd className="mt-1 text-tremor-metric font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
				{value}
			</dd>
			{subtitle && (
				<p
					className={cn(
						"mt-1 text-tremor-default",
						trend === "positive" && "text-emerald-600 dark:text-emerald-500",
						trend === "negative" && "text-red-600 dark:text-red-500",
						trend === "neutral" &&
							"text-tremor-content dark:text-dark-tremor-content",
						!trend && "text-tremor-content dark:text-dark-tremor-content",
					)}
				>
					{subtitle}
				</p>
			)}
		</Card>
	);
}
