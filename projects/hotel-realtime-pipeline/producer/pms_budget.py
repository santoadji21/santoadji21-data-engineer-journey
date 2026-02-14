import json
import time
import random
import os
from datetime import datetime
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
    # Budget Format: Flat, integer dates, minimal fields
    check_in = fake.date_between(start_date='today', end_date='+14d')
    # Convert date to integer YYYYMMDD
    date_int = int(check_in.strftime("%Y%m%d"))
    
    return {
        "bk_ref": fake.bothify(text='??-####'),
        "client": fake.name(),
        "start_date": date_int,
        "stay_len": random.randint(1, 3),
        "cost": random.randint(50, 150), # Integer cost, no cents
        "source": "PMS_BUDGET"
    }

def run():
    producer = get_producer()
    print("💰 PMS Budget (Minimalist) started...")
    try:
        while True:
            event = generate_event()
            producer.send(TOPIC, event)
            print(f"[Budget] Sent: {event['bk_ref']}")
            time.sleep(random.uniform(1, 3))
    except KeyboardInterrupt:
        print("Stopping Budget PMS...")

if __name__ == "__main__":
    run()
