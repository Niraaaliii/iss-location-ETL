import pandas as pd
from datetime import datetime
import time
import logging
import argparse
from typing import Dict, Any
from store_data import setup_database, store_iss_data, read_iss_data
from fetch_iss_data import fetch_iss_location
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/iss_tracker.log'),
        logging.StreamHandler()
    ]
)

def create_location_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    """Create a DataFrame from ISS location data"""
    return pd.DataFrame({
        'timestamp': [datetime.fromtimestamp(data['timestamp'])],
        'latitude': [float(data['iss_position']['latitude'])],
        'longitude': [float(data['iss_position']['longitude'])]
    })

def collect_iss_data(engine, duration_seconds: int = 300, interval_seconds: int = 30) -> None:
    """
    Collect ISS location data for specified duration and interval
    
    Args:
        engine: SQLAlchemy engine instance
        duration_seconds: Total duration to collect data (default: 300s)
        interval_seconds: Interval between collections (default: 30s)
    """
    logging.info(f"Starting ISS location collection for {duration_seconds} seconds...")
    end_time = time.time() + duration_seconds
    
    try:
        while time.time() < end_time:
            try:
                data = fetch_iss_location()
                df = create_location_dataframe(data)
                store_iss_data(engine, df)
                logging.info(f"Stored location at: {df['timestamp'][0]}")
                time.sleep(interval_seconds)
            except Exception as e:
                logging.error(f"Error collecting data: {str(e)}")
                time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logging.info("Data collection stopped by user")

def main() -> None:
    parser = argparse.ArgumentParser(description='ISS Location Tracker')
    parser.add_argument('--duration', type=int, default=300,
                      help='Duration in seconds to collect data (default: 300)')
    parser.add_argument('--interval', type=int, default=30,
                      help='Interval in seconds between collections (default: 30)')
    args = parser.parse_args()

    try:
        engine = setup_database()
        collect_iss_data(engine, args.duration, args.interval)
        
        stored_data = read_iss_data(engine)
        logging.info("\nAll stored ISS locations:")
        print(stored_data)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
