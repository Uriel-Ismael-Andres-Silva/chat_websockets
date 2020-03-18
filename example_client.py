import asyncio
import websockets
import ip
import time,os,json

class Cliente:
    
    def __init__(self):
        self.conexion=time.strftime("%H:%M:%S")
        self.clean=self.get_variable_to_clean()
        self.ws=None
        
    async def main(self):
        uri = "ws://localhost:8765"
        
        async with websockets.connect(uri) as websocket:
            await websocket.send(self.verify())
                
            verify=await websocket.recv()
            if verify == 'True':
                print("----------Hola como estas, Ahora puedes empezar a mandar textos---------")
            elif verify == 'False':
                if websocket.open==True:
                    print("esta encendido") 
                    await websocket.send(self.register("uriel"))

                else:
                    print("esta apagado")
                    ws= await self.reconnect(websocket)
                    if self.ws.open==True:
                        print("ya esta encendido")
                        
                        
                """async with websockets.connect(uri) as websocket:
                    name=input("Escriba su nombre de usuario: ")
                    await websocket.send(self.register(name))
                    register=await websocket.recv()
                    if register=='True':
                        print("---Usuario Registado con Exito----")"""
                        
                
    async def reconnect(self,web):
        uri = "ws://localhost:8765"
        try:
            self.ws=await websockets.connect(uri)
        except Exception as ex:
            
            print("Error de conexion: ",ex)
 
    def get_variable_to_clean(self):
        if os.name == "posix":
            return "clear"
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            return "cls"
       
    def verify(self):
        return self.conv_json({"reason":"verify","ip":ip.getIp()})
    
    def register(self,nombre):
        return self.conv_json({"reason":"register","ip":ip.getIp(),"user":nombre})

    
    def conv_json(self,data):
        return json.dumps(data)


cliente=Cliente()
asyncio.get_event_loop().run_until_complete(cliente.main())