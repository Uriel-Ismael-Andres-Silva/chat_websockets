import psycopg2
from db_config import get_configuration_data

class Conexion:
    def __init__(self):
        global conection,params#variables globales
        conection=None
        params=get_configuration_data()#obtener los parametros de configuracion de bd
    def connect(self):
        conection=psycopg2.connect(**params)
        return conection
    def disconnect(self):
         if conection is not None:
            try:
                conection.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: ", error)

