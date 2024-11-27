import websockets
import json
import datetime
import asyncio



class ServerSocket():
    def __init__(self,host,port) -> None:
        self.host = host
        self.port = port
        self.clients = set()
        
    async def register(self,websocket):
        if(websocket):
            self.clients.add(websocket)
            
    async def remove(self,websocket):
        if(websocket):
            self.clients.remove(websocket)
            
    async def broadcast(self,message):
        if(message):
            for client in self.clients:
                await client.send(message)
                
    async def handle_client(self,web_socket):
        try:
            await self.register(web_socket)
            async for message in web_socket:
                try:
                    data = json.loads(message)
                    
                    response = {
                        "msg":data["msg"],
                        "time":datetime.datetime.now().isoformat()
                    }

                    await self.broadcast(json.dumps(response))
                except json.JSONDecodeError:
                    print("INVALID JSON")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.remove(web_socket)
    
    async def start(self):
        print("starting server .............\n \n")
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        print(f"websocket server started on host::{self.host}:{self.port}")
        
        await server.wait_closed()
        

async def main():
    socket = ServerSocket("localhost",5000)
    await socket.start()
    
    
if __name__ == "__main__":
    asyncio.run(main())
    
            
        
            