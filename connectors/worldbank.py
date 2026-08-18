import requests


class WorldBankConnector:

    BASE_URL = "https://api.worldbank.org/v2"

    def get_indicator(self, country_code, indicator):

        url = (
            f"{self.BASE_URL}/country/{country_code}"
            f"/indicator/{indicator}"
            "?format=json&per_page=10"
        )

        try:

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if len(data) < 2:
                return None

            for record in data[1]:

                if record["value"] is not None:
                    return record["value"]

            return None

        except Exception as e:

            print("Error:", e)
            return None

    def get_population(self, country_code):

        return self.get_indicator(
            country_code,
            "SP.POP.TOTL"
        )

    def get_gdp(self, country_code):

        return self.get_indicator(
            country_code,
            "NY.GDP.MKTP.CD"
        )