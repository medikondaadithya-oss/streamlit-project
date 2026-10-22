import streamlit as st
import requests

# Page settings
st.set_page_config(page_title="Weather API Demo", page_icon="🌦️")

st.title("🌦️ Weather API Demo")
st.write("Get live weather information for a city.")

# API key: use Streamlit secrets if configured
try:
    saved_key = st.secrets["API_KEY"]
except Exception:
    saved_key = ""

API_KEY = st.text_input(
    "Enter OpenWeather API Key",
    value=saved_key,
    type="password"
)

# City input
city = st.text_input("Enter City", "Chennai")

# Get weather
if st.button("Get Weather"):

    if not API_KEY.strip():
        st.error("Please enter your API key.")
    elif not city.strip():
        st.error("Please enter a city name.")
    else:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city.strip(),
            "appid": API_KEY.strip(),
            "units": "metric"
        }

        response = None

        try:
            with st.spinner("Fetching weather..."):
                response = requests.get(
                    url, params=params, timeout=10
                )
                response.raise_for_status()
                data = response.json()

            # Extract weather details
            weather = {
                "City": data["name"],
                "Temperature": data["main"]["temp"],
                "Condition": data["weather"][0]["description"].title(),
                "Humidity": data["main"]["humidity"]
            }

            # Display JSON
            st.subheader("Weather Data (JSON)")
            st.json(weather)

            # Display metrics
            c1, c2, c3 = st.columns(3)

            c1.metric("Temperature", f"{weather['Temperature']} °C")
            c2.metric("Condition", weather["Condition"])
            c3.metric("Humidity", f"{weather['Humidity']}%")

        except requests.exceptions.Timeout:
            st.error("Request timed out. Try again.")

        except requests.exceptions.HTTPError:
            if response is not None and response.status_code == 404:
                st.error("City not found. Check the city name.")
            elif response is not None and response.status_code == 401:
                st.error("Invalid API key. Check your key.")
            else:
                st.error("Weather API returned an HTTP error.")

        except requests.exceptions.RequestException:
            st.error("Network error. Check your internet connection.")

        except (KeyError, ValueError, IndexError):
            st.error("Could not read the weather data.")

# HTTP methods
st.markdown("---")
st.subheader("HTTP Methods")

st.write("**GET** - Retrieve data")
st.write("**POST** - Send data")
st.write("**PUT** - Update data")
st.write("**DELETE** - Delete data")