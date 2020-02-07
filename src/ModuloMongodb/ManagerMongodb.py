from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime


class ManagerMongoDb:

    def __init__(self):
        self.MONGO_URL_ATLAS = 'mongodb+srv://Alvaro:alvareitor@cluster0-bcw38.mongodb.net/test?retryWrites=true&w=majority'

        self.cliente: MongoClient = None
        self.db: Database = None
        self.coleccion: Collection = None

    def conectarDB(self, db, coleccion):
        self.cliente = MongoClient(self.MONGO_URL_ATLAS, ssl_cert_reqs=False)
        self.db = self.cliente[db]
        self.coleccion = self.db[coleccion]

    def nuevo_registro(self, fecha, concepto, valor):
        registrar = self.coleccion.insert_one({
            "fecha": fecha,
            "concepto": concepto,
            "valor": valor
        })
        if registrar.inserted_id != None:
            return "Evento registrado con éxito"
        else:
            return "No posible registro"

    def busqueda_DB(self):
        busqueda = self.coleccion.find({})
        return busqueda

    def getinforme(self, fecha_inicio_informe, fecha_fin_informe):

        historico = list(self.coleccion.find(
            {
                "fecha": {
                    "$gte": fecha_inicio_informe,
                    "$lte": fecha_fin_informe
                }
            })
        )
        return historico


managermongo = ManagerMongoDb()
managermongo.conectarDB(db="examen03", coleccion="examen03")
