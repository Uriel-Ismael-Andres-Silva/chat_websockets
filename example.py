import asyncio,websockets,json
from usuario import Usuario
from mensaje import Mensaje
from multiprocessing import Process,Queue
from time import sleep

global user_list
user_list=[1]

class Server:
   
    def __init__(self):
        self.message_list=Queue()
        self.users_list=Queue()
        p1 = Process(target=self.get_data_messages, args=(self.message_list,))
        p2 = Process(target=self.get_data_users, args=(self.users_list,))
        p1.start()
        p2.start()

    def get_data_messages(self,cola):
        msg=Mensaje()
        while True:    
            data_msg=msg.getAllMessages()
            cola.put(data_msg)

            sleep(5)
  
    def get_data_users(self,cola):
        user=Usuario()
        while True:
            data_user=user.getAllUsers()
            cola.put(data_user[0])
            #print("dentro de funcion usuarios: ",cola.get())
            sleep(5)

    async def verify(self,ip):
        user=Usuario()
        res=await user.verify(ip)
        return res
    async def register(self,ip,u):
        user=Usuario()
        res=await user.register_User(ip,u)
        return res

    async def main(self,websocket, path):
        data=json.loads(await websocket.recv())
        reason=data["reason"]
        if reason=='verify':
            await websocket.send(str(await self.verify(data["ip"])))
        elif reason=='register':
            await websocket.send(str(await self.register(data["ip"],data["user"])))

server=Server()
loop = asyncio.get_event_loop()
start_serve=websockets.serve(server.main,'localhost',8765)
loop.run_until_complete(start_serve)
print("servidor encendido")
try:
    loop.run_forever()
except Exception as ex:
    print(ex)

