from connectors.worldbank import WorldBankConnector

wb = WorldBankConnector()

print(wb.get_population("DZ"))

print(wb.get_gdp("DZ"))