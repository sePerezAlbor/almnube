import pandas as pd
from pymongo import MongoClient

df_ = pd.read_csv('Accidentedes_Barranquilla_victimas.csv', encoding='utf-8')
print(df_.head())

url = "mongodb+srv://perezalborsebastian:RHoAddewAZXIFILD@cluster0.klofmwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&connectTimeoutMS=30000&socketTimeoutMS=30000"
client = MongoClient(url)

db = client['proyecto_personal']
coleccion = db['Accidentedes_Barranquilla_victimas.csv']
print('Base de datos: proyecto_personal')
print('Coleccion: Accidentedes_Barranquilla_victimas.csv')

coleccion.insert_many(df_.to_dict('records'))
print('Datos insertados correctamente')

print('\n Primeros 3 documentos en MongoDB: ')
for doc in coleccion.find().limit(3):
    print(doc)

total = coleccion.count_documents({})
print(f"\n Total de registros en la colección: {total}")