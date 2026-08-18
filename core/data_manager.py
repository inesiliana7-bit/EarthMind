from connectors.worldbank import WorldBankConnector

from connectors.openmeteo import OpenMeteoConnector


class DataManager:

    def __init__(self):

        self.worldbank = WorldBankConnector()

        self.weather = OpenMeteoConnector()


    def get_country_data(self, country_name, wb_code, latitude, longitude):

        data = {

            "Country": country_name,

            "Population": self.worldbank.get_population(wb_code),

            "GDP": self.worldbank.get_gdp(wb_code),

            "Weather": self.weather.get_weather(

                latitude,
   
                longitude

            )

        }

        return data