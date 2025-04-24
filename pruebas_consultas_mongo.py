from pymongo import MongoClient

url = "mongodb+srv://perezalborsebastian:RHoAddewAZXIFILD@cluster0.klofmwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url)

db = client["sample_mflix"]
peliculas = db["movies"]

print("\n Conectado a MongoDB Atlas exitosamente.")
print("Base de datos: sample_mflix")
print("Colección: movies\n")

print("Primer documento en la colección:")
print(peliculas.find_one())

print("\nPrimeras 5 películas:")
for peli in peliculas.find().limit(5):
    print(f"- {peli.get('title', 'Sin título')} ({peli.get('year', 'Sin año')})")

print("\n Películas del año 1995:")
for peli in peliculas.find({"year": 1995}).limit(3):
    print(f"- {peli.get('title')}")

print("\n Películas producidas en Colombia:")
for peli in peliculas.find({"countries": "Colombia"}).limit(3):
    print(f"- {peli.get('title')} - Países: {peli.get('countries')}")

print("\n Películas del género Drama:")
for peli in peliculas.find({"genres": "Drama"}).limit(3):
    print(f"- {peli.get('title')} - Géneros: {peli.get('genres')}")

total = peliculas.count_documents({})
colombianas = peliculas.count_documents({"countries": "Colombia"})

print(f"\n Total de películas en la colección: {total}")
print(f" Total de películas colombianas: {colombianas}")