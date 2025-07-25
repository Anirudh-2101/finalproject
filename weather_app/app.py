import streamlit as st
import requests
from datetime import datetime
import pytz
import matplotlib.pyplot as plt

# Constants
API_KEY = "a94859982c0d069f6db671303c549831"  # From your JavaScript code; replace if invalid
CURRENT_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Functions
def get_weather_data(city, units):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units
    }
    try:
        res = requests.get(CURRENT_URL, params=params)
        res.raise_for_status()  # Raise an error for bad responses (e.g., 401, 404)
        print("Current Weather Response:", res.json())  # Debug: Print API response
        return res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching current weather: {str(e)}")
        return {"cod": "error", "message": str(e)}

def get_forecast_data(city, units):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units
    }
    try:
        res = requests.get(FORECAST_URL, params=params)
        res.raise_for_status()  # Raise an error for bad responses
        print("Forecast Response:", res.json())  # Debug: Print API response
        return res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast: {str(e)}")
        return {"cod": "error", "message": str(e)}

def format_time(utc_time, timezone_offset):
    try:
        local_time = datetime.utcfromtimestamp(utc_time + timezone_offset)
        return local_time.strftime('%I:%M %p')
    except Exception as e:
        st.error(f"Error formatting time: {str(e)}")
        return "N/A"

def main():
    st.title("🌦️ Real-Time Weather App")
    city = st.text_input("Enter City Name", "Bangalore, IN")  # Default to Bangalore, IN
    unit_toggle = st.radio("Choose Unit", ('Celsius', 'Fahrenheit'))
    units = 'metric' if unit_toggle == 'Celsius' else 'imperial'
    unit_symbol = '°C' if unit_toggle == 'Celsius' else '°F'

    if city:
        weather = get_weather_data(city, units)
        forecast = get_forecast_data(city, units)

        # Check for API errors
        if weather.get("cod") != 200:
            st.error(f"Error: {weather.get('message', 'City not found or invalid API key. Please check the name and API key.')}")
            st.write("If you see 'Invalid API key', visit https://openweathermap.org/faq#error401 for help.")
            return

        # Display current weather
        st.subheader(f"Current Weather in {weather['name']}")
        st.write(f"**Temperature:** {weather['main']['temp']} {unit_symbol}")
        st.write(f"**Humidity:** {weather['main']['humidity']}%")
        st.write(f"**Condition:** {weather['weather'][0]['description'].capitalize()}")

        # Display weather icon
        try:
            icon = weather['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            st.image(icon_url)
        except KeyError:
            st.warning("Weather icon not available.")

        # Sunrise and sunset
        try:
            timezone_offset = weather['timezone']
            sunrise = format_time(weather['sys']['sunrise'], timezone_offset)
            sunset = format_time(weather['sys']['sunset'], timezone_offset)
            st.write(f"**Sunrise:** {sunrise}")
            st.write(f"**Sunset:** {sunset}")
        except KeyError:
            st.warning("Sunrise/sunset data not available.")

        # Forecast Chart
        if forecast.get("cod") == "200":
            st.subheader("5-Day Forecast (Every 3 Hours)")
            temps = []
            times = []
            try:
                for item in forecast['list']:
                    temps.append(item['main']['temp'])
                    time = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
                    times.append(time.strftime('%m-%d %Hh'))

                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(times, temps, marker='o', color='blue')
                plt.xticks(rotation=45)
                ax.set_title('Temperature Forecast')
                ax.set_ylabel(f'Temp ({unit_symbol})')
                ax.grid(True)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error plotting forecast: {str(e)}")
        else:
            st.error(f"Forecast error: {forecast.get('message', 'Unable to fetch forecast data.')}")

if __name__ == "__main__":
    main()