
import sys
import os


import latchsrc.latch as latch
import base64


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

APP_ID = os.environ.get("APP_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")
WEB3WALLET = "" 
WEB3SIGNATURE = ""


def get_error_message(response):
    if response == None:
        return ''
    error = response.get_error()
    if error != "":
        errorMsg = f"Error in request with error_code: {response.get_error().get_code()}"
        + f" and message: {response.get_error().get_message()}"
        print(errorMsg)
        return errorMsg
    else:
        return ''

def handle_response_data(response):
    if response == None:
        return ''
    errorMsg = get_error_message(response)
    if errorMsg != "":
        return errorMsg
    else:
        return response.data

def pair(pairing_code):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.pair(pairing_code, WEB3WALLET, WEB3SIGNATURE)
    errorMsg = get_error_message(response)
    if errorMsg != "":
        return errorMsg
    else:
        account_id = response.data.get("accountId")
        return account_id


def unpair(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.unpair(account_id)
    return handle_response_data(response)


def status(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.status(account_id)
    return handle_response_data(response)

def lock(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.lock(account_id)
    return handle_response_data(response)

def unlock(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.unlock(account_id)
    return handle_response_data(response)

def history(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.history(account_id)
    return handle_response_data(response)

def totp_create(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.totp_create(account_id)
    # Example how to decode the qr
    # imageData = response.data['qr'][len("data:image/png;base64,"):]
    # decoded = base64.b64decode(imageData)
    # filename = "qr.png"
    # with open(filename, "wb") as f:
    #     f.write(decoded)
    return handle_response_data(response)

def operation(account_id):
    api = latch.Latch(APP_ID, SECRET_KEY)
    response = api.operation(account_id)
    return handle_response_data(response)