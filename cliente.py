import asyncio
import websockets
import ip
import time,os,json
from datetime import datetime

class Cliente:
    def __init__(self):
        self.ws = websockets.WebSocketClientProtocol
        self.clean=self.get_variable_to_clean()
        self.url = 'ws://192.168.0.179:8000'
        self.users_list=[]
        self.messages_list=[]
        self.status_verify=None
        
    
    """async def main(self):
        try:                
            self.ws = await websockets.connect(self.url)
            await self.ws.send(self.verify())
            verify=await self.ws.recv()
            if verify=='True':
                print("----------Hola como estas, Ahora puedes empezar a mandar textos---------")
            elif verify == 'False':
                name=input("Escribe tu nombre de Usuario: ")
                await self.reconnect()
                    
                await self.ws.send(self.register(name))
                register=await self.ws.recv()
                if register=='True':
                    print("Usuario Registrado Exitosamente")
                    await asyncio.sleep(3)
                    os.system(self.clean)
                    while True:
                        os.system(self.clean)
                        #await self.getMessages()
                        await self.sendMessage()
                        await asyncio.sleep(5)
                        
                    #await self.sendMessage()

        except Exception as ex:
            print("Error en el main: ", ex)"""

    async def handler(self):
        await self.conexion()
        
        #Primer paso verificar si el usuario ya esta registrado
        
        await self.enviar(self.verify())
        await self.recibir()

        if self.status_verify=='True':
            print("Bienvenido al Chat")
        elif self.status_verify=='False':
            print("Creo que aun no estas registrado")
    
    async def enviar(self,data):
        try:
            if self.ws.open:
                await self.ws.send(data)
            else:
                print("Socket cerrado")
        except Exception as ex:
            print("Error al enviar los datos al servidor: ",ex)
            
    
    async def recibir(self):
        response=json.loads(await self.ws.recv())
        print(type(response))
        reason=response["reason"]
                
        if reason=='get_messages':
            pass
        elif reason=='get_users':
            pass
        elif reason=='verification_response':
            print("verificando")
            self.status_verify=response["response"]
        elif reason=='registration_response':
            pass
        elif reason=='response_message_added':
            pass
        elif reason=='last_time':
            pass

        
        
        
    async def getMessages(self):
        await self.reconnect()
        await self.ws.send(self.messages())
        messages=await self.ws.recv()
        print(messages)
        
    async def sendMessage(self):
        await self.reconnect()
        await self.ws.send(self.add_messages(input("->")))
    
    async def reconnect(self):
        try:
            self.ws = await websockets.connect(self.url)
        except Exception as ex:
            print("Error en la reconexion: ", ex)
    async def conexion(self):
        try:
            self.ws = await websockets.connect(self.url)
        except Exception as ex:
            print("Error en la conexion: ", ex)

    def get_variable_to_clean(self):
        if os.name == "posix":
            return "clear"
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            return "cls"

    def verify(self):
        return self.conv_json({"reason": "verify", "ip": ip.getIp()})

    def register(self, nombre):
        return self.conv_json({"reason": "register", "ip": ip.getIp(), "user": nombre})
    
    def messages(self):
        return self.conv_json({"reason": "messages"})
    
    def add_messages(self,mensaje):
        #datos1 = {'ip' : '192.168.0.179'}
        datos2 = {'ip' : '192.168.0.17'}
        #lista=[datos1,datos2]
        lista=[datos2]
        json_str = json.dumps(lista)
        ahora = datetime.now()
        #return self.conv_json({"reason": "add_message","message":mensaje,"ip":ip.getIp(),"receptor":json_str,"ahora":str(ahora)})
        return self.conv_json({"reason": "add_message","message":mensaje,"ip":"192.168.0.17","receptor":json_str,"ahora":str(ahora)})

    def conv_json(self, data):
        return json.dumps(data)


cliente = Cliente()
loop = asyncio.get_event_loop()
loop.run_until_complete(cliente.handler())
