from requests import get
import pandas as pd
from datetime import tzinfo
import psycopg2
from psycopg2.extras import execute_values
import os
import time

def get_wind_data(station_id:str = "VS1721") -> dict | None:
    url = f"https://portwind.no/api/v1/dbdata-seconds.php?stationid={station_id}&dataset=wswd&seconds=60"
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error getting wind data: {response.status_code}")
        return None
    
def parse_wind_data(data):

    df = pd.DataFrame(data['data'])

    # Convert Unix timestamp (milliseconds) to datetime with proper timezone handling
    df['timestamp_utc'] = pd.to_datetime(df['uts'], unit='ms', utc=True)

    # Convert from UTC to local time
    df['timestamp_local'] = df['timestamp_utc'].dt.tz_convert('Europe/Oslo')#.dt.tz_localize(None)

    # Remove time zone information
    df['timestamp_utc'] = df['timestamp_utc']#.dt.tz_localize(None)
    # Drop the original uts column and reorder
    df = df.drop('uts', axis=1)

    return df

def insert_wind_data(df):
    # Database connection parameters
    try:
        # Connect to the database
        CONNECTION = os.getenv('DATABASE_URL', 'postgres://user:password@postgres:5432/mydb')
        conn = psycopg2.connect(CONNECTION)
        cur = conn.cursor()
        
        # Prepare data for insertion
        data_to_insert = [
            (row['timestamp_utc'], row['station_id'], row['wind_speed'], row['wind_direction'])
            for _, row in df.iterrows()
        ]
        # Insert data using execute_values for better performance
        insert_query = """
            INSERT INTO wind_measurements (timestamp, station_id, wind_speed, wind_direction)
            VALUES %s
            ON CONFLICT DO NOTHING
        """
        
        execute_values(cur, insert_query, data_to_insert)
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(data_to_insert)} wind measurements")
        
    except Exception as e:
        print(f"Error inserting data into database: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    while True:
        station_id = "VS1721"
        starion_ids = ["VS1721", 'VS1596', 'VS1595', 'VS1722']
        start = time.time()
        for station_id in starion_ids:
            data = get_wind_data(station_id)
            if data:
                df = parse_wind_data(data)
                df['station_id'] = station_id
                insert_wind_data(df)
                print("Data ingestion completed for station: ", station_id)
            time.sleep(2)
        
        time.sleep(60 - (time.time() - start)) # Sleep until the next full minute
        
if __name__ == "__main__":
    main()
