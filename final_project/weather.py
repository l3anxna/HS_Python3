import os
import requests
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")

def fetch_weather_data(lat, lon, date, endpoint="history"):
    BASE_URL = f"https://api.weatherapi.com/v1/{endpoint}.json"
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "dt": date.strftime("%Y-%m-%d") if endpoint == "history" else None,
        "days": 3 if endpoint == "forecast" else None,
        "aqi": "yes",
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return None

def save_to_csv(data, filename, historical=False):
    all_data = []
    if historical:
        date = data["forecast"]["forecastday"][0]["date"]
        for hour in data["forecast"]["forecastday"][0]["hour"]:
            all_data.append(
                {
                    "Date": date,
                    "Hour": hour["time"].split(" ")[1],
                    "Temperature (°C)": hour["temp_c"],
                    "Humidity (%)": hour["humidity"],
                    "Precipitation (mm)": hour.get("precip_mm", 0),
                    "AQI (US)": hour.get("air_quality", {}).get("us-epa-index", "N/A"),
                }
            )
    else:
        for day in data["forecast"]["forecastday"]:
            date = day["date"]
            for hour in day["hour"]:
                all_data.append(
                    {
                        "Date": date,
                        "Hour": hour["time"].split(" ")[1],
                        "Temperature (°C)": hour["temp_c"],
                        "Humidity (%)": hour["humidity"],
                        "Precipitation (mm)": hour.get("precip_mm", 0),
                        "AQI (US)": hour.get("air_quality", {}).get(
                            "us-epa-index", "N/A"
                        ),
                    }
                )

    df = pd.DataFrame(all_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def load_from_csv(filename, selected_date):
    df = pd.read_csv(filename)
    df = df[df["Date"] == selected_date]
    return {
        "hour": df["Hour"].to_numpy(),
        "temperature": df["Temperature (°C)"].to_numpy(),
        "humidity": df["Humidity (%)"].to_numpy(),
        "precipitation": df["Precipitation (mm)"].to_numpy(),
    }

def plot_weather_data(processed_data, date):
    hours = np.arange(len(processed_data["hour"]))
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(
        hours,
        processed_data["temperature"],
        label="Temperature (°C)",
        marker="o",
        color="orange",
    )
    plt.fill_between(
        hours,
        processed_data["temperature"] - np.std(processed_data["temperature"]),
        processed_data["temperature"] + np.std(processed_data["temperature"]),
        alpha=0.2,
        color="orange",
        label="Temperature Std Dev",
    )
    plt.title(f"Temperature Trend on {date}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Temperature (°C)")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(
        hours,
        processed_data["humidity"],
        label="Humidity (%)",
        color="blue",
        marker="s",
    )
    plt.title(f"Humidity Trend on {date}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Humidity (%)")
    plt.legend()

    plot_filename = f'static/plot_{date}.png'
    plt.savefig(plot_filename)
    plt.close(fig)
    return plot_filename

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_weather():
    city_coords = {
        "London": {"lat": 51.5074, "lon": -0.1278},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Tokyo": {"lat": 35.6895, "lon": 139.6917},
        "Paris": {"lat": 48.8566, "lon": 2.3522},
        "Mumbai": {"lat": 19.076, "lon": 72.8777},
        "Beijing": {"lat": 39.9042, "lon": 116.4074},
        "Sydney": {"lat": -33.8688, "lon": 151.2093},
        "Dubai": {"lat": 25.276987, "lon": 55.296249},
        "Bangkok": {"lat": 13.7563, "lon": 100.5018},
        "Manchester": {"lat": 53.4808, "lon": -2.2426},
        "Kyiv": {"lat": 50.4501, "lon": 30.5234},
        "Odesa": {"lat": 46.4825, "lon": 30.7233},
    }

    city = request.form['city']
    option = request.form['option']
    
    if city not in city_coords:
        return 'City not found in database.'

    lat, lon = city_coords[city]["lat"], city_coords[city]["lon"]

    if option == '1':
        date_input = request.form['date']
        
        try:
            selected_date = datetime.strptime(date_input, "%Y-%m-%d")
            if (
                selected_date > datetime.now()
                or selected_date < datetime.now() - timedelta(days=7)
            ):
                return 'Date must be within the past 7 days.'

            historical_data = fetch_weather_data(lat, lon, selected_date)

            if historical_data:
                filename = f"{city}_historical_weather.csv"
                save_to_csv(historical_data, filename, historical=True)
                processed_data = load_from_csv(filename, date_input)
                plot_filename = plot_weather_data(processed_data, date_input)

                return render_template('result.html', plot_url=plot_filename)

            else:
                return 'Failed to retrieve data.'
        
        except ValueError:
            return 'Invalid date format. Please use YYYY-MM-DD.'

    elif option == '2':
        forecast_data = fetch_weather_data(lat, lon, date=None, endpoint="forecast")

        if forecast_data:
            filename = f"{city}_3_day_forecast_aqi.csv"
            save_to_csv(forecast_data, filename)

            dates = [day["date"] for day in forecast_data["forecast"]["forecastday"]]
            return render_template('select_date.html', dates=dates)

@app.route('/visualize', methods=['POST'])
def visualize_forecast():
    city_coords = {
        "London": {"lat": 51.5074, "lon": -0.1278},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Tokyo": {"lat": 35.6895, "lon": 139.6917},
        "Paris": {"lat": 48.8566, "lon": 2.3522},
        "Mumbai": {"lat": 19.076, "lon": 72.8777},
        "Beijing": {"lat": 39.9042, "lon": 116.4074},
        "Sydney": {"lat": -33.8688, "lon": 151.2093},
        "Dubai": {"lat": 25.276987, "lon": 55.296249},
        "Bangkok": {"lat": 13.7563, "lon": 100.5018},
        "Manchester": {"lat": 53.4808, "lon": -2.2426},
        "Kyiv": {"lat": 50.4501, "lon": 30.5234},
        "Odesa": {"lat": 46.4825, "lon": 30.7233},
     }

    city = request.form['city']
    selected_date = request.form['selected_date']
    lat, lon = city_coords[city]["lat"], city_coords[city]["lon"]

    forecast_data = fetch_weather_data(lat, lon, date=None, endpoint="forecast")
    filename = f"{city}_3_day_forecast_aqi.csv"
    save_to_csv(forecast_data, filename)

    processed_data = load_from_csv(filename, selected_date)
    plot_filename = plot_weather_data(processed_data, selected_date)

    return render_template('result.html', plot_url=plot_filename)

if __name__ == '__main__':
   app.run(debug=True)
