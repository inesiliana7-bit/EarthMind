from core.data_fusion import collect_all_sources

data = collect_all_sources("Algeria")

print(data.keys())

print(len(data["news"]))

print(len(data["nasa"]))