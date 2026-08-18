from core.data_manager import DataManager

manager = DataManager()

country = manager.get_country_data(

    "Algeria",

    "DZ",

    36.7538,

    3.0588

)

print(country)