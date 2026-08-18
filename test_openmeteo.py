from connectors.openmeteo import OpenMeteoConnector

weather = OpenMeteoConnector()

result = weather.get_weather(

    36.7538,

    3.0588

)

print(result)