from typing import List
from starlette.websockets import WebSocket

class ConnectionManager():
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            if connection.client_state.value == 1:
                print("Sending: connection open: " + str(message))
                await connection.send_text(message)
            else:
                print("Not sending: connection closed")
                # CAUSED MISSING CALLS: self.active_connections.remove(connection)

        

manager = ConnectionManager()