from pymongo import MongoClient
url = "mongodb+srv://perezalborsebastian:RHoAddewAZXIFILD@cluster0.klofmwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url)
print("Bases de datos disponibles: ")
print(client.list_database_names())