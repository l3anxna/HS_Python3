import os
import requests
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("No API key found.")


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/index")
def index():
    return render_template("index.html")


def fetch_weather_data(city_name, date=None):
    BASE_URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}"

    if date:
        BASE_URL += f"/{date.strftime('%Y-%m-%d')}"
    else:
        BASE_URL += "/next15days"

    params = {
        "unitGroup": "metric",
        "key": API_KEY,
        "contentType": "json",
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
    all_data = []

    if "days" not in data:
        print("No 'days' data found in the response.")
        return

    for day in data["days"]:
        if "hours" not in day:
            print(f"No 'hours' data found for {day.get('datetime', 'unknown date')}.")
            continue

        for hour in day["hours"]:
            all_data.append(
                {
                    "Date": day["datetime"],
                    "Hour": hour["datetime"],
                    "Temperature (°C)": hour["temp"],
                    "Humidity (%)": hour["humidity"],
                    "Precipitation (mm)": hour.get("precip", 0),
                    "UV Index": hour.get("uvindex", "N/A"),
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
        "UV Index": df["UV Index"].to_numpy(),
    }


def plot_weather_data(processed_data, date, city_name):
    hours = np.arange(len(processed_data["hour"]))

    temperature = processed_data["temperature"]
    humidity = processed_data["humidity"]
    uv_index = processed_data.get("UV Index", np.zeros(len(hours)))

    # Check for valid indices
    valid_indices = ~np.isnan(temperature) & ~np.isnan(humidity) & ~np.isnan(uv_index)

    if not np.any(valid_indices):  # If no valid data is available
        raise ValueError("No valid weather data available for plotting.")

    fig, ax = plt.subplots(3, 1, figsize=(12, 12))

    ax[0].plot(
        hours[valid_indices],
        temperature[valid_indices],
        label="Temperature (°C)",
        marker="o",
        color="orange",
    )
    ax[0].set_title(f"{city_name} Temperature Trend on {date}")
    ax[0].set_xlabel("Hour of the Day")
    ax[0].set_ylabel("Temperature (°C)")
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(
        hours[valid_indices],
        humidity[valid_indices],
        label="Humidity (%)",
        color="blue",
        marker="s",
    )
    ax[1].set_title(f"{city_name} Humidity Trend on {date}")
    ax[1].set_xlabel("Hour of the Day")
    ax[1].set_ylabel("Humidity (%)")
    ax[1].legend()
    ax[1].grid(True)

    ax[2].plot(
        hours[valid_indices],
        uv_index[valid_indices],
        label="UV Index",
        color="purple",
        marker="x",
    )
    ax[2].set_title(f"{city_name} UV Index Trend on {date}")
    ax[2].set_xlabel("Hour of the Day")
    ax[2].set_ylabel("UV Index")
    ax[2].legend()
    ax[2].grid(True)

    plt.tight_layout()

    plot_filename = f"static/plot_{date}.png"
    plt.savefig(plot_filename)
    plt.close(fig)

    pie_chart_filename = plot_pie_chart(processed_data)

    summary = {
        "average_temperature": np.nanmean(temperature),
        "average_humidity": np.nanmean(humidity),
        "total_precipitation": np.nansum(processed_data["precipitation"]),
    }

    return plot_filename, summary, pie_chart_filename



def plot_pie_chart(processed_data):
    temperature_bins = [-np.inf, 10, 20, np.inf]
    temperature_counts = np.histogram(processed_data["temperature"], bins=temperature_bins)[0]

    humidity_bins = [-np.inf, 40, 70, np.inf]
    humidity_counts = np.histogram(processed_data["humidity"], bins=humidity_bins)[0]

    # Check for empty counts
    if np.all(temperature_counts == 0) or np.all(humidity_counts == 0):
        raise ValueError("No valid data available for pie chart.")

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    axs[0].pie(
        temperature_counts,
        labels=["Cold", "Moderate", "Hot"],
        autopct="%1.1f%%",
        startangle=90,
    )
    axs[0].set_title("Temperature Categories")

    axs[1].pie(
        humidity_counts,
        labels=["Dry", "Pleasant", "Humid"],
        autopct="%1.1f%%",
        startangle=90,
    )
    axs[1].set_title("Humidity Categories")

    plt.tight_layout()

    pie_chart_filename = "static/pie_chart.png"
    
    plt.savefig(pie_chart_filename)
    plt.close(fig)

    return pie_chart_filename


def generate_weather_summary(processed_data):
    temperature = processed_data["temperature"]
    humidity = processed_data["humidity"]

    summary = (
        f"The day starts with a temperature of {temperature[0]:.2f}°C and ends at {temperature[-1]:.2f}°C. "
        f"The highest temperature is {temperature.max():.2f}°C and the lowest is {temperature.min():.2f}°C. "
        f"Humidity levels range from {humidity.min()}% to {humidity.max()}%."
    )

    return summary


@app.route("/fetch", methods=["POST"])
def fetch_weather():
    city_name = request.form.get("city")
    option = request.form.get("option")

    if option == "1":
        date_input = request.form.get("date")

        if not date_input:
            return "Date input cannot be empty. Please select a date."

        try:
            selected_date = datetime.strptime(date_input, "%Y-%m-%d")
            if selected_date > datetime.now():
                return "Cannot fetch forecast data for past dates."
            historical_data = fetch_weather_data(city_name, selected_date)

            if not historical_data:
                return "Failed to retrieve weather data. Please try again later."

            filename = f"{city_name}_historical_weather.csv"
            save_to_csv(historical_data, filename)
            processed_data = load_from_csv(filename, date_input)

            if processed_data:
                plot_filename, summary, pie_chart_filename = plot_weather_data(
                    processed_data, date_input, city_name
                )
                weather_summary = generate_weather_summary(processed_data)

                summary_text = (
                    f"Average Temperature: {summary['average_temperature']:.2f}°C<br>"
                    f"Average Humidity: {summary['average_humidity']:.2f}%<br>"
                    f"Total Precipitation: {summary['total_precipitation']:.2f} mm<br>"
                )

                return render_template(
                    "result.html",
                    plot_url=plot_filename,
                    pie_chart_url=pie_chart_filename,
                    summary=summary_text + "<br>" + weather_summary,
                )

            return "Failed to process the weather data."

        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

    elif option == "2":
        date_input = request.form.get("date")

        if not date_input:
            return "Date input cannot be empty. Please select a date."

        try:
            selected_date = datetime.strptime(date_input, "%Y-%m-%d")
            forecast_data = fetch_weather_data(city_name, selected_date)

            if not forecast_data:
                return "Failed to retrieve weather data. Please try again later."

            filename = f"{city_name}_forecast_weather.csv"
            save_to_csv(forecast_data, filename)
            processed_data = load_from_csv(filename, date_input)

            if processed_data:
                plot_filename, summary, pie_chart_filename = plot_weather_data(
                    processed_data, date_input, city_name
                )
                weather_summary = generate_weather_summary(processed_data)

                summary_text = (
                    f"Average Temperature: {summary['average_temperature']:.2f}°C<br>"
                    f"Average Humidity: {summary['average_humidity']:.2f}%<br>"
                    f"Total Precipitation: {summary['total_precipitation']:.2f} mm<br>"
                )

                return render_template(
                    "result.html",
                    plot_url=plot_filename,
                    pie_chart_url=pie_chart_filename,
                    summary=summary_text + "<br>" + weather_summary,
                )

            return "Failed to process the weather data."

        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."


if __name__ == "__main__":
    app.run(debug=True)
