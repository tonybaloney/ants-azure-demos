# FastAPI on PyPy

This example project is a Docker image running PyPy3.9 with FastAPI demonstrating how to host an API
using PyPy as the Python interpreter

- Includes a VS Code dev container for local development
- Includes a debug profile for VS Code
- Includes a Dockerfile for deployment into Azure Web Apps

## Deployment

Setup some variables

```console
RG=my-web-app  # Resource group name
ACR=myregistry1  # Azure Container Registry name
IMAGE=my-web-app # Docker image name
NAME=my-web-app # Application name, also used as the DNS record
LOCATION=australiaeast # DC location
```

Create the Azure resource group and container registry:

```console
az group create --location $LOCATION --name $RG
az acr create --name $ACR --resource-group $RG --sku Basic --admin-enabled true
az acr credential show --name $ACR
```

Sign in to the container registry with those credentials. Build and upload the Docker image:

```console
docker login ${ACR}.azurecr.io
docker build -t ${IMAGE}:1.0.0 .
docker tag ${IMAGE}:1.0.0 ${ACR}.azurecr.io/${IMAGE}:1.0.0
docker push ${ACR}.azurecr.io/${IMAGE} -a
```

Create an Azure Container Instance and deploy from the Docker image:

```console
az container create --resource-group $RG --name $NAME --image ${ACR}.azurecr.io/${IMAGE}:1.0.0 --dns-name-label $NAME --ports 80
az container attach --resource-group $RG --name $NAME
open http://${NAME}.${LOCATION}.azurecontainer.io/
```


Optional: Add a CNAME record to an Azure DNS managed zone

```console
az network dns record-set cname set-record -g $RG -z www.mysite.com  -n MyRecordSet -c ${NAME}.${LOCATION}.azurecontainer.io
```
