from core.data_manager import DataManager
from core.data_processor import DataProcessor

manager = DataManager()

processor = DataProcessor()

raw = manager.get_country_data(

    "Algeria",

    "DZ",

    36.7538,

    3.0588

)

processed = processor.process(raw)

print(processed)