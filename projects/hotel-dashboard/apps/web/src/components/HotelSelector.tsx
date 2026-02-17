import type { HotelSummary } from "@/lib/types";
import { Select, SelectItem } from "@tremor/react";

interface HotelSelectorProps {
	hotels: HotelSummary[];
	selected: string | null;
	onSelect: (hotelId: string | null) => void;
}

export function HotelSelector({
	hotels,
	selected,
	onSelect,
}: HotelSelectorProps) {
	return (
		<Select
			value={selected ?? "all"}
			onValueChange={(val) => onSelect(val === "all" ? null : val)}
			placeholder="Select a hotel"
		>
			<SelectItem value="all">All Hotels</SelectItem>
			{hotels.map((hotel) => (
				<SelectItem key={hotel.hotel_id} value={hotel.hotel_id}>
					{hotel.hotel_name}
				</SelectItem>
			))}
		</Select>
	);
}
