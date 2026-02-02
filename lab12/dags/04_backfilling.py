import pendulum
import requests
import pandas as pd
import os
from datetime import timedelta
from airflow.sdk import dag, task

LATITUDE = 40.7143
LONGITUDE = -74.006
FILE_PATH = "new_york_weather.csv"


@dag(
    dag_id="backfilling_weather_forecast",
    start_date=pendulum.datetime(2025, 1, 1, tz="America/New_York"),
    schedule=timedelta(days=7),
    catchup=True,
    tags=["exercise_2", "weather", "backfill"],
)
def weather_backfill_pipeline():
    @task
    def get_forecast(**kwargs) -> dict:
        start_date_str = kwargs["ds"]

        start_date_obj = pendulum.parse(start_date_str)
        end_date_obj = start_date_obj.add(days=6)
        end_date_str = end_date_obj.to_date_string()

        print(f"Fetching data for interval: {start_date_str} to {end_date_str}")

        url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "daily": ["temperature_2m_max", "temperature_2m_min"],
            "timezone": "auto"
        }

        resp = requests.get(url, params=params)
        resp.raise_for_status()

        return resp.json()

    @task
    def transform(data: dict) -> pd.DataFrame:
        daily_data = data.get("daily")

        df = pd.DataFrame({
            "date": daily_data.get("time"),
            "min_temp": daily_data.get("temperature_2m_min"),
            "max_temp": daily_data.get("temperature_2m_max")
        })

        return df

    @task
    def save_results(df: pd.DataFrame) -> None:
        print(f"Saving {len(df)} rows to {FILE_PATH}")

        file_exists = os.path.isfile(FILE_PATH)

        df.to_csv(FILE_PATH, mode="a", index=False, header=not file_exists)

    raw_data = get_forecast()
    clean_data = transform(raw_data)
    save_results(clean_data)


weather_backfill_pipeline()