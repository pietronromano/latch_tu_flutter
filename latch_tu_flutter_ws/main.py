'''
Websockets sample for FastAPI
FastAPI handles both Websockets routes (via Starlette wrapper) and HTML responses
https://github.com/Azure/app-service-linux-docs/blob/master/HowTo/WebSockets/use_websockets_with_fastapi.md
'''

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from connections import manager
import uvicorn


app = FastAPI()

# Websockets url: local (ws = new WebSocket('ws://localhost:8001/ws');) 
# Azure: wss://latchtuflutterws.azurewebsites.net/ws
html = """
<h1>Real Time Messaging</h1>
<pre id="messages" style="height: 400px; overflow: scroll"></pre>
<input type="text" id="messageBox" placeholder="Type your message here" style="display: block; width: 100%; margin-bottom: 10px; padding: 10px;" />
<button id="send" title="Send Message!" style="width: 100%; height: 30px;">Send Message</button>

<script>
  (function() {
    const sendBtn = document.querySelector('#send');
    const messages = document.querySelector('#messages');
    const messageBox = document.querySelector('#messageBox');

    let ws;

    function showMessage(message) {
      messages.textContent += `\n\n${message}`;
      messages.scrollTop = messages.scrollHeight;
      messageBox.value = '';
    }

    function init() {
      var opened = false;
      if (ws) {
        ws.onerror = ws.onopen = ws.onclose = null;
        ws.close();
      }

      //ws = new WebSocket('ws://localhost:8001/ws');
      ws = new WebSocket('wss://latchtuflutterws.azurewebsites.net/ws');
      ws.onopen = () => {
        console.log('Connection opened!');
        opened = true;
      }

      ws.onmessage = ({ data }) => showMessage(data);
      ws.onclose = function() {
        ws = null;
      }
      ws.onerror = function(error) {
        console.log(error);
      }
    }

    sendBtn.onclick = function() {
      if (!ws) {
        showMessage("No WebSocket connection :(");
        return ;
      }

      ws.send(messageBox.value);
    }

    init();
  })();
</script>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)


###########################
@app.get("/webhook", response_class=PlainTextResponse)
async def verify_challenge(challenge: str): 
    return challenge

@app.post("/webhook")
async def receive_notification(request: Request): 
    while True:
        try:
          json = await request.json()
          jsonString = str(json)
          await manager.broadcast({jsonString})
          return jsonString
        except Exception as e:
          print('error: ', e)
          break

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(websocket.url.path)
    print(websocket.url.port)
    print(websocket.url.scheme)

    await manager.connect(websocket)
    while True:
        try:
          data = await websocket.receive_text()
          await manager.broadcast({data})
          
        except Exception as e:
          print('error: ', e)
          break

###############################

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001)