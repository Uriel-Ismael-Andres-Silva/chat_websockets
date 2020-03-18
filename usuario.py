import aiopg
import asyncio,json
from datetime import datetime
from conexion import Conexion

class Usuario:
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
        
              
    def getAllUsers(self):
        lista=[]
        lista_ip=[]
        lst=[]
        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.execute('SELECT * FROM cat.users')
                usuarios = cursor.fetchall()
                for usuario in usuarios:
                    datos={"id":usuario[0],"ip":usuario[1],"usuario":usuario[2],"hora":str(usuario[3])}
                    json_datos = json.dumps(datos)
                    lista.append(json.loads(json_datos))
                    dato_ip={"ip":usuario[1]}
                    json_datos_ip = json.dumps(dato_ip)
                    lista_ip.append(json.loads(json_datos_ip))
                
                lst=[lista,lista_ip]
        except Exception as e:
            print("Error: ", e)
        else:
            return lst
        finally:
            cursor.close()
            conexion.disconnect()
            
        
    async def update_Last_Time(self,ahora,ip):
        try:
            if await self.con():
                await self.cur.callproc('cat.updatelastseen',(ip,ahora))
        except Exception as e:
            print("Error: ", e)
            return False
        else:
            return True
        finally:
            self.cur.close()
            self.conn.close()

    async def verify(self,ip):
        try:
            if await self.con():
                await self.cur.callproc('cat.verificar',(ip,))
                row = await self.cur.fetchone()
                if row[0]==0:
                    return False         
        except Exception as e:
            print("Error: ", e)
            return False
        else:
            return True
        finally:
            self.cur.close()
            self.conn.close()
    
    
    async def register_User(self,ip,nombre):
        ahora = datetime.now() 
        try:
            if await self.con():
                await self.cur.callproc('cat.adduser',(ip,nombre,ahora))
        except Exception as e:
            print("Error en funcion: ", e)
            return False
        else:
            return True
        finally:
            self.cur.close()
            self.conn.close() 
            
        
    """async def main(self):
        await self.register_User("192.168.0.179","Uriel")
        #print(await self.verify('192.168.0.179'))
        await self.getUsers()
        #ahora=datetime.now()
        #await self.update_Last_Time(ahora,'192.168.0.179')

user = Usuario()
loop = asyncio.get_event_loop()
loop.run_until_complete(user.main())"""
#user=Usuario()
#print(user.getAllUsers())
