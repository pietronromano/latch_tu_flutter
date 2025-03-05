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
This is deployed as Azure Web App for Containers, which were found to be more reliable for Web Sockets.
For deployment with the Azure CLI, use the following commands:

See this link for a general example on dpeloying an App with ACR:
https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container?tabs=azure-portal&pivots=container-linux


## Create an ACR
```
az acr create --name <registry-name> --resource-group  latchtuflutter-rg  --sku Basic --admin-enabled true
az acr credential show --resource-group latchtuflutter-rg --name <registry-name>

az acr credential show --resource-group  latchtuflutter-rg --name <registry-name>
docker login <registry-name>.azurecr.io --username <registry-username>
```

## Create a User-Assigned Managed Identity
az identity create --name myID --resource-group  latchtuflutter-rg

## Docker Image
Use the commands below to build and run the FastAPI in a Docker image: Specify platform to avoid "no matching manifest for linux/amd64"
```
docker build -t latchtuflutter --platform linux/x86_64 . 

docker run -p 8001:8001 latchtuflutter  --name latchtuflutter
```

## Azure Container Registry:
```
az acr login -n latchtuflutter  -u latchtuflutter -p <pwd>
docker tag latchtuflutter latchtuflutter.azurecr.io/latchtuflutter:v1
docker push latchtuflutter.azurecr.io/latchtuflutter:v1
```

## Create the Web App
```
az appservice plan create --name latchtuflutterPlan --resource-group latchtuflutter-rg --is-linux
az webapp create --resource-group latchtuflutter-rg --plan latchtuflutterPlan --name latchtuflutterws--deployment-container-image-name <registry-name>.azurecr.io/latchtuflutter:v1
az webapp config appsettings set --resource-group latchtuflutter-rg --name latchtuflutterws --settings WEBSITES_PORT=8001
id=$(az identity show --resource-group latchtuflutter-rg --name myID --query id --output tsv)
az webapp identity assign --resource-group latchtuflutter-rg --name latchtuflutterws  --identities $id
appConfig=$(az webapp config show --resource-group latchtuflutter-rg --name latchtuflutterws  --query id --output tsv)
az resource update --ids $appConfig --set properties.acrUseManagedIdentityCreds=True
clientId=$(az identity show --resource-group latchtuflutter-rg --name myID --query clientId --output tsv)
az resource update --ids $appConfig --set properties.AcrUserManagedIdentityID=$clientId

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