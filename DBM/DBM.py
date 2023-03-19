from pymongo import MongoClient


class MongoDB_admin():
    def __init__(self,password,db,collection,usuario=None):
        self.password =  password
        self.db = db
        self.collection = collection
        self.usuario = usuario
        
    def insert_documents(self,documents):
        connection_string = f"mongodb+srv://coderchemivan:{self.password}@cluster0.mp5mmin.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client[self.db]
        
        #creat collection if not exists
        if self.collection not in db.list_collection_names():
            db.create_collection(self.collection)
            col = self.collection
            #create index con los campos de nombre y año
            db[col].create_index([('titulo',1),('año',1),('usuario',1)],unique=True)
        self.collection = db[self.collection]
        self.collection.insert_many(documents,ordered=False)

    def get_documents(self):
        connection_string = f"mongodb+srv://coderchemivan:{self.password}@cluster0.mp5mmin.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string)
        db = client[self.db]
        self.collection = db[self.collection]
        return self.collection.find({'usuario':self.usuario})