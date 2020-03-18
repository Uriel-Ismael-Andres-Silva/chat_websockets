import asyncio
import websockets
from websockets.exceptions import *

class Servidor:
    def __init__(self):
        self.conectados=[]
    
    async def main(self,ws,path):
        self.conectados.append(ws)
        try:
            data=await ws.recv()
            print("dato recibido desde el cliente: ",data)
            await ws.send("hola cliente como estas")
            await ws.send("otro mensaje")

        except ConnectionClosedError as ex:
            self.conectados.remove(ws)
            print("Error: ",ex)
        
servidor=Servidor()

loop=asyncio.get_event_loop()
on_server=websockets.serve(servidor.main,'localhost',8000)
loop.run_until_complete(on_server)
print("Servidor Funcionando.....")
try:
    loop.run_forever()
except Exception as ex:
    print("Error en el servidor: ",ex)
