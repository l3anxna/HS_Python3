import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = os.getenv("d267cdf65b4e44a3b6a21013252701")
print(f"Using API Key: {API_KEY}")

def fetch_weather_data(lat, lon, date):
    BASE_URL = "https://api.weatherapi.com/v1/history.json"
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "dt": date.strftime("%Y-%m-%d")
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

def save_to_csv(data, filename):
    hourly_data = []
    for hour in data["forecast"]["forecastday"][0]["hour"]:
        hourly_data.append({
            "Hour": hour["time"].split(" ")[1],
            "Temperature (°C)": hour["temp_c"],
            "Humidity (%)": hour["humidity"],
            "Precipitation (mm)": hour.get("precip_mm", 0)
        })
    
    df = pd.DataFrame(hourly_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def load_from_csv(filename):
    df = pd.read_csv(filename)
    return {
        "temperature": df["Temperature (°C)"].to_numpy(),
        "humidity": df["Humidity (%)"].to_numpy(),
        "precipitation": df["Precipitation (mm)"].to_numpy()
    }

def plot_weather_data(processed_data, date):
    hours = np.arange(24)
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(hours, processed_data["temperature"], label="Temperature (°C)", marker="o")
    plt.fill_between(hours,
                     processed_data["temperature"] - processed_data["temperature"].std(),
                     processed_data["temperature"] + processed_data["temperature"].std(),
                     alpha=0.2, color="orange", label="Temperature Std Dev")
    plt.title(f"Temperature Trend on {date}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    
    plt.subplot(2, 1, 2)
    ax1 = plt.gca()
    
    ax1.plot(hours, processed_data["humidity"], label="Humidity (%)", color="blue", marker="s")
    ax1.set_ylabel("Humidity (%)", color="blue")
    
    ax2 = ax1.twinx()
    ax2.bar(hours, processed_data["precipitation"], alpha=0.6, label="Precipitation (mm)", color="green")
    ax2.set_ylabel("Precipitation (mm)", color="green")
    
    plt.title(f"Humidity and Precipitation Trends on {date}")
    
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Welcome to the Weather Trends Visualization Tool!")
    
    city_coords = {
        "London": {"lat": 51.5074, "lon": -0.1278},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Tokyo": {"lat": 35.6895, "lon": 139.6917},
    }

    city = input("Enter city name (e.g., London): ")
    
    if city not in city_coords:
        print("City not found in database.")
        exit()

    lat, lon = city_coords[city]["lat"], city_coords[city]["lon"]
    
    date_input = input("Enter a date (YYYY-MM-DD) for historical weather data: ")
    
    try:
        date = datetime.strptime(date_input, "%Y-%m-%d")
        
        print(f"Fetching weather data for {city} on {date_input}...")
        weather_data = fetch_weather_data(lat, lon, date)

        if weather_data:
            filename = f"{city}_{date_input}.csv"
            save_to_csv(weather_data, filename)

            processed_data = load_from_csv(filename)
            plot_weather_data(processed_data, date_input)
        else:
            print("Failed to retrieve data.")
            
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
