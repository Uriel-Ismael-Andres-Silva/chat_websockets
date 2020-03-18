import aiopg
import asyncio,json
from conexion import Conexion
from datetime import datetime


class Mensaje:

    def __init__(self):
        global conexion
        conexion = Conexion()
        self.conn = None
        self.cur=None
        
    async def con(self):
        try:
            self.conn = await aiopg.connect(database='bootcamp',user='postgres',password='postgresql',host='35.192.187.11')        
            self.cur = await self.conn.cursor()
            return True
        except Exception as ex:
            return False
        
    def getAllMessages(self):
        lista=[]
        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.callproc('cat.getallmessages')
                mensajes = cursor.fetchall()
                for mensaje in mensajes:
                    datos={"id":mensaje[0],"message":mensaje[1],"emisor":mensaje[2],"receptor":mensaje[3],"hora_fecha":str(mensaje[4])}
                    json_datos = json.dumps(datos)
                    lista.append(json.loads(json_datos))
                
        except Exception as e:
            print("Error: ", e)
        else:
            return lista
        finally:
            cursor.close()
            conexion.disconnect()
    
    
    async def addMessage(self,mensaje,emisor,receptor,fecha_hora):
        try:
            if await self.con():
                await self.cur.callproc('cat.addmessage',(mensaje,emisor,receptor,fecha_hora))
        except Exception as e:
            print("Error: ", e)
            return False
        else:
            return True
        finally:
            self.cur.close()
            self.conn.close() 
            
        
    """async def main(self):
        datos1 = {
            'ip' : '192.168.0.179'
        }
        datos2 = {
            'ip' : '192.168.0.17'
        }
        lista=[datos1,datos2]

        json_str = json.dumps(lista)

        ahora = datetime.now() 

        await self.addMessage("Hola, Como Estan Grupo?","192.168.0.179",json_str,ahora)
        #await self.getAllMessages()


msg = Mensaje()
loop = asyncio.get_event_loop()
loop.run_until_complete(msg.main())"""

#msg=Mensaje()
#print(msg.getAllMessages())
