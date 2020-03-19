import asyncio,websockets,json
from websockets.exceptions import *
from usuario import Usuario
from mensaje import Mensaje
from multiprocessing import Process,Queue
from time import sleep

class Servidor:
    def __init__(self):
        self.conectados = []
        self.message_list = Queue()
        self.users_list = Queue()
        self.ip_list=Queue()
        self.ip_conexion=None
        self.data_ws=[]
        p1 = Process(target=self.get_data_messages, args=(self.message_list,))
        p2 = Process(target=self.get_data_users, args=(self.users_list,self.ip_list))
        p1.start()
        p2.start()

    def get_data_messages(self, cola):
        msg = Mensaje()
        while True:
            data_msg = msg.getAllMessages()
            cola.put(data_msg)
            sleep(5)

    def get_data_users(self, cola,cola2):
        user = Usuario()
        while True:
            data_user = user.getAllUsers()
            cola.put(data_user[0])
            cola2.put(data_user[1])
            sleep(5)

    async def getFilterMessages(self):
        while True:
            for usuario in self.conectados:
                print("estoy en ciclo")
                print(len(self.conectados))
                msgs=[]
                for msg in self.message_list:
                    print("recorriendo lista de mensajes")
                    if msg["emisor"]==usuario.remote_address:
                        print("el emisor es el del mensaje")
                        msgs.append(msg)
                    else:
                        receptores=msg["receptor"] 
                        for receptor in receptores:
                            print("el receptor es el del mensaje")
                            if receptor["ip"]==usuario.remote_address:
                                msgs.append(msg)
                              
                else:         
                    print("no hay mensajes")
            else:
                print("No hay Usuarios")
                
            await asyncio.sleep(5)
                        
    
    def sendMessagesClient(self,usuario,msgs):
        try:
            usuario.send(msgs)
        except Exception as ex:
            print("Error al enviar mensaje al cliente: ",ex)
    
    async def add_message(self,mensaje,emisor,receptor,ahora):
        msg=Mensaje()
        res=await msg.addMessage(mensaje,emisor,receptor,ahora)
        return res

    async def verify(self, ip):
        user = Usuario()
        res = await user.verify(ip)
        response=self.conv_json({"reason":'verification_response',"response":str(res)})
        return response

    async def register(self, ip, u):
        user = Usuario()
        res = await user.register_User(ip, u)
        return res

    def conv_json(self, data):
        return json.dumps(data)
            
    async def main(self, ws, path):
        await self.verify_and_register_websocket(ws)        
        data = json.loads(await ws.recv())
        try:
            reason = data["reason"]
            if reason == 'verify':
                print("entro en verificacion")
                await ws.send(str(await self.verify(data["ip"])))
            elif reason == 'register':
                await ws.send(str(await self.register(data["ip"], data["user"])))
                self.conectados.remove(ws)
            elif reason=='messages':
                await ws.send(str(self.getFilterMessages()))
            elif reason=='add_message':
                if data["receptor"]=='all':
                    res=await self.add_message(data["message"],data["ip"],self.ip_list,data["ahora"])
                else:
                    res=await self.add_message(data["message"],data["ip"],data["receptor"],data["ahora"])
                self.conectados.remove(ws)

              
                  
        except ConnectionClosedError as ex:
            print("Error: ", ex)
                 
    async def verify_and_register_websocket(self,ws):
        if len(self.conectados)==0:
            self.conectados.append(ws)
            data=self.conv_json({"ip": ws.remote_address, "num_msg": 0})
            self.data_ws.append(data)
        else:
            for webs in self.conectados:
                if webs.remote_address == ws.remote_address:
                    self.conectados.remove(webs)
                    self.conectados.append(ws)
            else:
                self.conectados.append(ws)
                data=self.conv_json({"ip": ws.remote_address, "num_msg": 0})
                self.data_ws.append(data)



on_server = websockets.serve(servidor.main, '192.168.0.179', 8000)
loop.run_until_complete(on_server)
print("Servidor Funcionando.....")
try:
    loop.run_forever()
except Exception as ex:
    print("Error en el servidor: ", ex)
