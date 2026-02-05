import csv
import random
from datetime import datetime, timedelta

def generate_hotel_data(num_records=100):
    hotels = ['Grand Plaza', 'Ocean View', 'Mountain Retreat', 'City Hub']
    room_types = ['Standard', 'Deluxe', 'Suite']
    
    start_date = datetime(2026, 1, 1)
    
    data = []
    for i in range(num_records):
        hotel = random.choice(hotels)
        room_type = random.choice(room_types)
        check_in = start_date + timedelta(days=random.randint(0, 30))
        stay_nights = random.randint(1, 7)
        check_out = check_in + timedelta(days=stay_nights)
        
        # Base price + room type premium + random variation
        base_price = 100
        premium = {'Standard': 0, 'Deluxe': 50, 'Suite': 150}
        price_per_night = base_price + premium[room_type] + random.randint(-10, 20)
        total_revenue = price_per_night * stay_nights
        
        data.append({
            'booking_id': f'BK{1000+i}',
            'hotel_name': hotel,
            'room_type': room_type,
            'check_in': check_in.strftime('%Y-%m-%d'),
            'check_out': check_out.strftime('%Y-%m-%d'),
            'stay_nights': stay_nights,
            'price_per_night': price_per_night,
            'total_revenue': total_revenue,
            'status': random.choices(['Checked-In', 'Cancelled', 'No-Show'], weights=[0.8, 0.15, 0.05])[0]
        })
    
    keys = data[0].keys()
    with open('data/raw_bookings.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    
    print(f"Generated {num_records} hotel booking records in data/raw_bookings.csv")

if __name__ == "__main__":
    generate_hotel_data(500)
