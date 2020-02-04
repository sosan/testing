from pymongo import MongoClient 
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime

class ManagerMongoDb:

    def __init__(self):
        self.MONGO_URL_ATLAS = 'mongodb+srv://Alvaro:alvareitor@cluster0-bcw38.mongodb.net/test?retryWrites=true&w=majority'
                                
        self.cliente: MongoClient = None
        self.db: Database = None
        self.coleccion : Collection = None
        
    def conectarDB(self,db,coleccion):
        self.cliente= MongoClient(self.MONGO_URL_ATLAS, ssl_cert_reqs= False)
        self.db = self.cliente[db]
        self.coleccion = self.db[coleccion]


    def busqueda_DB(self):
        busqueda = self.coleccion.find({})
        return busqueda
    



managermongo = ManagerMongoDb()
managermongo.conectarDB(db="examen03", coleccion="examen03")
