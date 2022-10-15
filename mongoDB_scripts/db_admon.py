import pymongo




# Replace the uri string with your MongoDB deployment's connection string.

class Admon_bd():
    def __init__(self,cluster,contraseña,db_name,collection_name):
        self.cluster = cluster
        self.contraseña = contraseña
        self.db_name = db_name
        self.collection_name = collection_name
        self.conn_str = "mongodb+srv://coderchemivan:{contraseña}@{cluster}.mp5mmin.mongodb.net/?retryWrites=true&w=majority".format(contraseña = self.contraseña,cluster= self.cluster)

        # set a 5-second connection timeout
        self.MONGO_BASEDATOS = self.db_name
        self.MONGO_COLECCION = self.collection_name

        try:
            cliente = pymongo.MongoClient(self.conn_str, serverSelectionTimeoutMS=5000)
            cliente.server_info()
            baseDatos=cliente[self.MONGO_BASEDATOS]
            coleccion=baseDatos[self.MONGO_COLECCION]
            cliente.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo exedido "+errorTiempo)

    def insertar_documeto(self,documento):
        try:
            cliente = pymongo.MongoClient(self.conn_str, serverSelectionTimeoutMS=5000)
            cliente.server_info()
            baseDatos=cliente[self.MONGO_BASEDATOS]
            coleccion=baseDatos[self.MONGO_COLECCION]
            coleccion.insert_one(documento)
            print("Inserción a mongo exitosa")
            cliente.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo exedido "+errorTiempo)


    def find_(self,documento):
        try:
            cliente = pymongo.MongoClient(self.conn_str, serverSelectionTimeoutMS=5000)
            cliente.server_info()
            baseDatos=cliente[self.MONGO_BASEDATOS]
            coleccion=baseDatos[self.MONGO_COLECCION]

            encontrados = []
            for documento_ in coleccion.find(documento):
                encontrados.append(documento_)
            if len(encontrados)>0:
                print("Encontrado_____________________-")
                return 1
            else:
                return 0
            cliente.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo exedido "+errorTiempo)





