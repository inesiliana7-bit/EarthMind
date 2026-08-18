from connectors.reliefweb import ReliefWebConnector

rw = ReliefWebConnector()

disasters = rw.get_disasters()

print("Number of disasters:", len(disasters))

if disasters:

    print(disasters[0]["fields"]["name"])