from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
import uvicorn

import latchsrc.latchmain as latchmain
import os


API_KEY = os.environ.get("API_KEY")
app = FastAPI()


########################### LATCH ###########
 
@app.get("/latch/pair/{code}")
async def latch_pair(code: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/pair/{code}")
    account_id = latchmain.pair(code)
    print(f"Result: {account_id}")
    return {"account_id": account_id}

@app.get("/latch/status/{account_id}")
async def latch_status(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/status/{account_id}")
    status = latchmain.status(account_id)
    print(f"Result: {str(status)}")
    return {"status": status['operations']}

@app.get("/latch/unpair/{account_id}")
async def latch_unpair(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/unpair/{account_id}")
    result = latchmain.unpair(account_id)
    print(f"Result: {str(result)}")
    return {"result": result}

@app.get("/latch/lock/{account_id}")
async def latch_lock(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/lock/{account_id}")
    result = latchmain.lock(account_id)
    print(f"Result: {str(result)}")
    return {"result": result}

@app.get("/latch/unlock/{account_id}")
async def latch_unlock(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/unlock/{account_id}")
    result = latchmain.unlock(account_id)
    print(f"Result: {str(result)}")
    return {"result": result}

@app.get("/latch/history/{account_id}")
async def latch_history(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/history/{account_id}")
    result = latchmain.history(account_id)
    print(f"Result: {str(result)}")
    return {"result": result}


@app.get("/latch/totp/create/{account_id}")
async def totp_create(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    print(f"Request: /latch/totp/create/{account_id}")
    result = latchmain.totp_create(account_id)
    print(f"Result: {str(result)}")
    return {"result": result}


@app.get("/latch/operation/{account_id}")
async def operation(account_id: str, x_api_key: Annotated[str, Header()] = None):
    if x_api_key == None or x_api_key != API_KEY:
        return 'Not Authorized'
    result = latchmain.operation(account_id)
    return {"result": result}



###########################
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

      setInterval(function () { 
          if(opened) {
            console.log('Pinging');
            ws.send("ping");
          }
        }, 10000);

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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

