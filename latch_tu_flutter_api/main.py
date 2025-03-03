from fastapi import FastAPI, Header, Request
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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

