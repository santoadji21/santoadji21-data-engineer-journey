import json
import time
import random
import uuid
import os
from datetime import datetime, timedelta
from kafka import KafkaProducer
from faker import Faker

fake = Faker()
TOPIC = "hotel_bookings"

def get_producer():
    return KafkaProducer(
        bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def generate_event():
    # Modern Format: Nested JSON, ISO dates, UUIDs
    check_in = fake.date_between(start_date='today', end_date='+60d')
    nights = random.randint(1, 14)
    check_out = check_in + timedelta(days=nights)
    
    return {
        "eventId": str(uuid.uuid4()),
        "guest": {
            "id": str(uuid.uuid4()),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email()
        },
        "booking": {
            "checkInDate": check_in.isoformat(),
            "checkOutDate": check_out.isoformat(),
            "roomType": random.choice(["DELUXE_SUITE", "STANDARD_VIEW", "PRESIDENTIAL"]),
            "totalPrice": round(random.uniform(200, 1000) * nights, 2),
            "currency": "USD"
        },
        "metadata": {
            "source": "PMS_MODERN",
            "version": "v2.0"
        }
    }

def run():
    producer = get_producer()
    print("✨ PMS Modern (The Startup) started...")
    try:
        while True:
            event = generate_event()
            producer.send(TOPIC, event)
            print(f"[Modern] Sent: {event['guest']['email']}")
            time.sleep(random.uniform(0.5, 2)) # Fast, modern system
    except KeyboardInterrupt:
        print("Stopping Modern PMS...")

if __name__ == "__main__":
    run()
