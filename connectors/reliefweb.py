import requests


class ReliefWebConnector:

    BASE_URL = "https://api.reliefweb.int/v1/disasters"

    def get_disasters(self):

        params = {

            "appname": "EarthMind",

            "limit": 10

        }

        try:

            response = requests.get(

                self.BASE_URL,

                params=params,

                timeout=20

            )

            response.raise_for_status()

            data = response.json()

            return data["data"]

        except Exception as e:

            print("ReliefWeb Error:", e)

            return []