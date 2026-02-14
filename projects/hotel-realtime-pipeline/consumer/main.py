import json
import time
import os
import pandas as pd
from kafka import KafkaConsumer
from datetime import datetime
from pathlib import Path

# Configuration
TOPIC = "hotel_bookings"
BOOTSTRAP_SERVERS = [os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')]
BATCH_SIZE = 50  # Number of messages to buffer before writing
DATA_DIR = Path("/app/data/raw")

def get_consumer():
    print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
    # Retry logic for startup
    while True:
        try:
            return KafkaConsumer(
                TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='earliest',
                group_id='lake_writer_group'
            )
        except Exception as e:
            print(f"Waiting for Kafka... ({e})")
            time.sleep(5)

def flush_batch(batch):
    if not batch:
        return

    # Create DataFrame
    # We store the RAW JSON as a string to handle schema drift/differences safely
    df = pd.DataFrame(batch)
    
    # Generate filename based on current time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = DATA_DIR / f"bookings_{timestamp}.parquet"
    
    # Ensure directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write to Parquet
    df.to_parquet(filename, engine='pyarrow', index=False)
    print(f"💾 Flushed {len(batch)} events to {filename}")

def run():
    consumer = get_consumer()
    print(f"🎧 Listening to {TOPIC}...")
    
    batch = []
    last_flush_time = time.time()
    
    for message in consumer:
        event = message.value
        
        # Add metadata
        row = {
            "ingestion_time": datetime.now(),
            "source_topic": TOPIC,
            "raw_data": json.dumps(event) # Store as string for Bronze Layer
        }
        
        batch.append(row)
        
        # Check buffer limits (Count or Time)
        current_time = time.time()
        if len(batch) >= BATCH_SIZE or (current_time - last_flush_time) > 60:
            flush_batch(batch)
            batch = []
            last_flush_time = current_time

if __name__ == "__main__":
    run()
