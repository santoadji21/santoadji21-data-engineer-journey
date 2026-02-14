import json
import time
import random
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
    # Legacy Format: Uppercase, cryptic keys, DD/MM/YYYY dates
    check_in = fake.date_between(start_date='today', end_date='+30d')
    return {
        "RES_ID": fake.random_int(min=10000, max=99999),
        "GUEST_NM": fake.name().upper(),
        "ARR_DT": check_in.strftime("%d/%m/%Y"),
        "NTS": random.randint(1, 7),
        "RM_TYP": random.choice(["KNG", "DBL", "TWN"]),
        "AMT": round(random.uniform(100, 500), 2),
        "SOURCE": "PMS_LEGACY"
    }

def run():
    producer = get_producer()
    print("🏨 PMS Legacy (Old School) started...")
    try:
        while True:
            event = generate_event()
            producer.send(TOPIC, event)
            print(f"[Legacy] Sent: {event['RES_ID']}")
            time.sleep(random.uniform(2, 5)) # Slower, older system
    except KeyboardInterrupt:
        print("Stopping Legacy PMS...")

if __name__ == "__main__":
    run()
