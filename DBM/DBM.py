from pymongo import MongoClient


class MongoDB_admin():
    def __init__(self,password,db,collection,usuario=None,movies_usuario=True):
        self.password =  password
        self.db = db
        self.collection = collection
        self.usuario = usuario
        self.movies_usuario = movies_usuario
        
    def insert_documents(self,documents):
        connection_string = f"mongodb+srv://coderchemivan:{self.password}@cluster0.mp5mmin.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client[self.db]
        
        #creat collection if not exists
        if self.collection not in db.list_collection_names():
            db.create_collection(self.collection)
            col = self.collection
            #create index con los campos de nombre y año
            if self.movies_usuario:
                db[col].create_index([('titulo',1),('año',1),('usuario',1)],unique=True)
            else:
                db[col].create_index([('titulo',1),('year',1),('director',1)],unique=True)
        self.collection = db[self.collection]
        self.collection.insert_many(documents,ordered=False)

    def get_documents(self,campo=None,valor=None):
        connection_string = f"mongodb+srv://coderchemivan:{self.password}@cluster0.mp5mmin.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client[self.db]
        self.collection = db[self.collection]
        return self.collection.find({campo:valor})
    
    def verificar_peliculas_existentes(self):
        connection_string = f"mongodb+srv://coderchemivan:{self.password}@cluster0.mp5mmin.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client[self.db]
        self.collection = db[self.collection]
        domain = 'https://letterboxd.com/'
        lista = [domain + film for film in self.collection.distinct('film_page')]
        return lista
    
#c =MongoDB_admin(password='bleistift16',db='movies',collection='watched').verificar_peliculas_existentes()
#print(c)