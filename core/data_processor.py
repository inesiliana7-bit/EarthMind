class DataProcessor:

    def process(self, data):

        weather = data["Weather"]

        processed = {

            "Country": data["Country"],

            "Population": data["Population"],

            "GDP": data["GDP"],

            "Temperature": weather["temperature_2m"],

            "Humidity": weather["relative_humidity_2m"],

            "Rain": weather["precipitation"],

            "Wind": weather["wind_speed_10m"]

        }

        return processed