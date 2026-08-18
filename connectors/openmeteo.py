import requests


class OpenMeteoConnector:

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude, longitude):

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m"
            ]

        }

        try:

            response = requests.get(

                self.BASE_URL,

                params=params,

                timeout=20

            )

            response.raise_for_status()

            return response.json()["current"]

        except Exception as e:

            print("OpenMeteo Error:", e)

            return None