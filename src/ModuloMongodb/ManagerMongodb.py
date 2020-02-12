from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime


class Errores:
    def __init__(self):
        self.correcto = 1
        self.duplicado = 2
        self.fallodb = 3


class ManagerMongoDb:

    def __init__(self):
        self.MONGO_URL_ATLAS = 'mongodb+srv://Alvaro:alvareitor@cluster0-bcw38.mongodb.net/test?retryWrites=true&w=majority'

        self.cliente: MongoClient = None
        self.db: Database = None
        self.coleccion: Collection = None
        self.coleccion_usuarios: Collection = None
        self.errores = Errores()

    def conectarDB(self, db, coleccion):
        self.cliente = MongoClient(self.MONGO_URL_ATLAS, ssl_cert_reqs=False)
        self.db = self.cliente[db]
        self.coleccion = self.db[coleccion]
        self.coleccion_usuarios = self.db["usuarios"]

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
            }).sort("fecha", 1))

        return historico

    def insert_default_conceptos(self, usuario):
        resultado = self.coleccion_usuarios.insert_one(
            {
                "conceptos_usuario": usuario,
                "conceptos": [
                    "Gasolina",
                    "Electricidad",
                    "Itv",
                    "Seguro",
                    "Frenos",
                    "Ruedas"
                ]

            }
        )

        if resultado.inserted_id != None:
            return True
        return False

    def getlistado_conceptos(self, usuario):
        listadoconceptos = self.coleccion_usuarios.find_one({"conceptos_usuario": usuario}, {"_id": False})

        if not listadoconceptos:
            resultado = self.insert_default_conceptos(usuario)
            if resultado == True:
                listadoconceptos = self.coleccion_usuarios.find_one({"conceptos_usuario": usuario}, {"_id": False})
                return listadoconceptos["conceptos"]
            else:
                return None
        else:
            return listadoconceptos["conceptos"]

    def insertar_nuevo_concepto(self, usuario, concepto):

        # primero miramos si existe el concepto:
        datos = self.coleccion_usuarios.find_one({"conceptos_usuario": usuario})
        if "conceptos" in datos:
            if concepto in datos["conceptos"]:
                # existe el concepto
                return self.errores.duplicado

        resultado = self.coleccion_usuarios.update_one(
            {"conceptos_usuario": usuario},
            {"$push": {
                "conceptos": concepto
            }}
        )

        if resultado.modified_count > 0:
            return self.errores.correcto
        return self.errores.fallodb


managermongo = ManagerMongoDb()
managermongo.conectarDB(db="examen03", coleccion="examen03")
