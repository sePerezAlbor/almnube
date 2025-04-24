from pymongo import MongoClient

# Conexión a MongoDB Atlas
url = "mongodb+srv://perezalborsebastian:RHoAddewAZXIFILD@cluster0.klofmwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&connectTimeoutMS=30000&socketTimeoutMS=30000"
client = MongoClient(url)

db = client['proyecto_personal']
collection = db['Accidentedes_Barranquilla_victimas.csv']

# Query 1 Total de registros 
total_records = collection.count_documents({})
print(" ")
print(f"Total de registros: {total_records}")

# Query 2 Total de registro por "SEXO_VICTIMA" de la victima
total_sexo = collection.aggregate([
    {
        "$group": {
            "_id": "$SEXO_VICTIMA",
            "total": {"$sum": 1}
        }
    }
])
print("\nTotal de registros por sexo de la víctima:")
for sexo in total_sexo:
    print(f"- {sexo['_id']}: {sexo['total']}")

#Query 3.1. Filtrar por año de accidente Fecha_Accidente

year = 2018
total_year = collection.count_documents({"Fecha_Accidente": {"$regex": f"^{year}-"}})
print(f"\nTotal de registros del año {year}: {total_year}")


#Query 3.2. Filtrar por año de accidente Fecha_Accidente

# year = 2018
# query = {"Fecha_Accidente": {"$regex": f"^{year}"}}
# result = collection.find(query)
# print(f"\nRegistros del año {year}:")
# for record in result:
#     print(record)

#Query 4 Top 5 valores más frecuentes de "CONDICION_VICTIMA"
top_condicion = collection.aggregate([
    {
        "$group": {
            "_id": "$CONDICION_VICTIMA",
            "total": {"$sum": 1}
        }
    },
    {
        "$sort": {"total": -1}
    },
    {
        "$limit": 5
    }
])
print("\nTop 5 condiciones de la víctima:")
for condicion in top_condicion:
    print(f"- {condicion['_id']}: {condicion['total']}")
print(" ")
