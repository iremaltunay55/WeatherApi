from dotenv import load_dotenv
import os
import requests

load_dotenv()

def getliveTemp(latitude, longitude):
    """
    Get live temperature for a given latitude and longitude.
    """
    try:
        # Get API key from environment variables
        WEATHER_API_KEY = "2a325d7d2c2e46dcaaf92754252105"
        if not WEATHER_API_KEY:
            return {"error": "API key not found in environment variables"}

        # Format location string
        location = f"{latitude},{longitude}"

        # Construct API URL
        api_url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"

        # Make the request
        response = requests.get(api_url)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract temperature from the response
            if "current" in data and "temp_c" in data["current"]:
                current_temp = data["current"]["temp_c"]
                return {
                    "temperature": current_temp,
                    "location": data["location"]["name"],
                    "country": data["location"]["country"],
                    "condition": data["current"]["condition"]["text"]
                }
            else:
                return {"error": "Temperature data not found in API response"}
        else:
            return {"error": f"Failed to retrieve data from API: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}