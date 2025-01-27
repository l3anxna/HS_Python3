import requests
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Replace with your own API key from OpenWeatherMap or WeatherAPI
API_KEY = "your_api_key"
BASE_URL = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

def fetch_weather_data(lat, lon, date):
    """
    Fetch historical weather data for a specific location and date.
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "dt": int(date.timestamp()),
            "appid": API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_csv(data, filename):
    """
    Save weather data to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Hour", "Temperature (°C)", "Humidity (%)", "Precipitation (mm)"])

        for i, hour in enumerate(data["hourly"]):
            temp = hour["temp"]
            humidity = hour["humidity"]
            precipitation = hour.get("rain", {}).get("1h", 0)  # Default to 0 if no rain data
            writer.writerow([i, temp, humidity, precipitation])

    print(f"Data saved to {filename}")

def load_from_csv(filename):
    """
    Load weather data from a CSV file.
    """
    data = {"temperature": [], "humidity": [], "precipitation": []}
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data["temperature"].append(float(row["Temperature (°C)"]))
            data["humidity"].append(float(row["Humidity (%)"]))
            data["precipitation"].append(float(row["Precipitation (mm)"]))
    return {key: np.array(value) for key, value in data.items()}

def plot_weather_data(processed_data, date):
    """
    Plot the processed weather data using Matplotlib.
    """
    hours = np.arange(24)
    
    # Temperature Plot
    plt.figure(figsize=(12, 6))
    plt.plot(hours, processed_data["temperature"], label="Temperature (°C)", marker="o")
    plt.fill_between(hours, 
                     processed_data["temperature"] - processed_data["temperature"].std(), 
                     processed_data["temperature"] + processed_data["temperature"].std(),
                     alpha=0.2, color="orange", label="Temperature Std Dev")
    plt.title(f"Temperature Trend on {date}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid()
    plt.show()

    # Humidity and Precipitation Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(hours, processed_data["humidity"], label="Humidity (%)", color="blue", marker="s")
    ax1.set_xlabel("Hour of the Day")
    ax1.set_ylabel("Humidity (%)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.bar(hours, processed_data["precipitation"], alpha=0.6, label="Precipitation (mm)", color="green")
    ax2.set_ylabel("Precipitation (mm)", color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    fig.suptitle(f"Humidity and Precipitation Trends on {date}")
    fig.legend(loc="upper right")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    print("Welcome to the Weather Trends Visualization Tool!")
    city = input("Enter city name (e.g., London): ")

    # Simulating city coordinates lookup (replace with real geocoding API if needed)
    city_coords = {
        "London": {"lat": 51.5074, "lon": -0.1278},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Tokyo": {"lat": 35.6895, "lon": 139.6917},
    }

    if city not in city_coords:
        print("City not found in database. Add coordinates for it manually.")
    else:
        lat, lon = city_coords[city]["lat"], city_coords[city]["lon"]

        # User input for date
        date_input = input("Enter a date (YYYY-MM-DD) for historical weather data: ")
        date = datetime.strptime(date_input, "%Y-%m-%d")

        print(f"Fetching weather data for {city} on {date_input}...")
        weather_data = fetch_weather_data(lat, lon, date)

        if weather_data:
            filename = f"{city}_{date_input}.csv"
            save_to_csv(weather_data, filename)

            # Load data from CSV and plot
            processed_data = load_from_csv(filename)
            plot_weather_data(processed_data, date_input)
        else:
            print("Failed to retrieve data. Please try again.")
