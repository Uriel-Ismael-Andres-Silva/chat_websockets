import asyncio
import websockets


class Cliente:
    def __init__(self):
        self.ws = websockets.WebSocketClientProtocol
        self.url = 'ws://localhost:8000'


    async def main(self):
        try:
            self.ws = await websockets.connect(self.url)
            
            try:
                await self.ws.send("holaaaa")
                print("m1: ",await self.ws.recv())


            except Exception as ex:
                await self.reconnect()
        except Exception as ex:
            print("Error en el main: ", ex)
            
            
    async def reconnect(self):
        try:
            self.ws=await websockets.connect(self.url)
        except Exception as ex:
            print("Error en la reconexion: ",ex)
        


cliente=Cliente()
loop=asyncio.get_event_loop()
loop.run_until_complete(cliente.main())
