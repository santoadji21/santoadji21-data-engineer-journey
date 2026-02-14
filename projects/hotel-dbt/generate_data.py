import pandas as pd
import json
import random
import uuid
import os
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

fake = Faker()
DATA_DIR = Path("/app/data/raw")

def generate_legacy():
    check_in = fake.date_between(start_date='today', end_date='+30d')
    return {
        "RES_ID": fake.random_int(min=10000, max=99999),
        "GUEST_NM": fake.name().upper(),
        "ARR_DT": check_in.strftime("%d/%m/%Y"),
        "NTS": random.randint(1, 7),
        "RM_TYP": random.choice(["KNG", "DBL", "TWN"]),
        "AMT": round(random.uniform(100, 500), 2),
        "SOURCE": "PMS_LEGACY",
        "source": "PMS_LEGACY" # Helper for dbt logic if needed, but we rely on json extraction usually
    }

def generate_modern():
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
        "metadata": {"source": "PMS_MODERN", "version": "v2.0"},
        "source": "PMS_MODERN"
    }

def generate_budget():
    check_in = fake.date_between(start_date='today', end_date='+14d')
    date_int = int(check_in.strftime("%Y%m%d"))
    return {
        "bk_ref": fake.bothify(text='??-####'),
        "client": fake.name(),
        "start_date": date_int,
        "stay_len": random.randint(1, 3),
        "cost": random.randint(50, 150),
        "source": "PMS_BUDGET"
    }

def run():
    print(f"Generating data into {DATA_DIR}...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    records = []
    # Generate 50 records of mixed types
    for _ in range(50):
        choice = random.choice(['legacy', 'modern', 'budget'])
        if choice == 'legacy':
            data = generate_legacy()
        elif choice == 'modern':
            data = generate_modern()
        else:
            data = generate_budget()
            
        # Simulate the structure stored by the Consumer (Raw JSON string)
        records.append({
            "ingestion_time": datetime.now(),
            "source_topic": "hotel_bookings",
            "raw_data": json.dumps(data)
        })
    
    df = pd.DataFrame(records)
    filename = DATA_DIR / f"test_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    df.to_parquet(filename, engine='pyarrow', index=False)
    print(f"✅ Created {filename} with 50 records.")

if __name__ == "__main__":
    run()
