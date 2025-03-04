# Latch tu Flutter
Repo for the tu Latch Innovation Contest

*Hacked by:* Pietro Romano, Copyright 2025

<br/>

# Structure of this Repo
This repo has the following main sections:
- **docs**: Powerpoint presentation and graphics used
- **latch_tu_flutter_api**: API implemented in Python with FastAPI, run on an Azure Web App
- **latch_tu_flutter_app**: Flutter client application that can be run on iOS, Android or other OSs.
- **latch_tu_flutter_ws**: Websockets implemented in Python with FastAPI, run on an Azure Web App
- **postman**: the Postman collection and environments used for testing

<br/>

# Configuration
## latch_tu_flutter_api
This is deployed as Azure Web App.
For deployment with the Azure CLI, use the following commands:
```
az login --tenant <TENANT>
az webapp up --runtime PYTHON:3.9 --sku B1 --logs --name <GLOBALLY UNIQUE APP NAME> --resource-group  latchtuflutter-rg --location westeurope
az webapp config set --startup-file "gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app" --name <GLOBALLY UNIQUE APP NAME>   --resource-group  latchtuflutter-rg
```

The following system variables need to be configured in the Web App Settings -> Environment Variables:
- `API_KEY`: key for authorizing calls to the API, used by the Flutter app
- `APP_ID`: the tu Latch Application ID
- `SECRET_KEY`: the tu Latch Secret

<br/>

## latch_tu_flutter_ws
This is deployed as Azure Web App.
For deployment with the Azure CLI, use the following commands:

```
az webapp up --sku B1 --name <GLOBALLY UNIQUE APP NAME>  --resource-group latchtuflutter-rg  --logs --runtime PYTHON:3.9
az webapp config set --name <GLOBALLY UNIQUE APP NAME>  --resource-group  latchtuflutter-rg --startup-file "gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app"

```

<br/>

## latch_tu_flutter_app
This is the Flutter app which communicates with latch_tu_flutter_api and latch_tu_flutter_ws.
The settings which need to be configured are all in the `lib/globals.dart` file:
````
String firebaseURL = '<URL OF FIREBASE REALTIME DATABASE>';

String apiURL = '<GLOBALLY UNIQUE APP NAME>.azurewebsites.net';
String apiKey = '<GUID>';
String wsURL = '<GLOBALLY UNIQUE APP NAME>.azurewebsites.net';
````