# FastAPI on PyPy

This example project is a Docker image running PyPy3.9 with FastAPI demonstrating how to host an API
using PyPy as the Python interpreter

- Includes a VS Code dev container for local development
- Includes a debug profile for VS Code
- Includes a Dockerfile for deployment into Azure Web Apps

## Deployment

Create the Azure resource group and container registry:

```console
az group create --location australiaeast --name pypy-testing
az acr create --name pypytesting --resource-group pypy-testing --sku Basic --admin-enabled true
az acr credential show --name pypytesting
```

Sign in to the container registry with those credentials. Build and upload the Docker image:

```console
docker login pypytesting.azurecr.io
docker build -t fastapi-hello-world:1.0.0 .
docker tag fastapi-hello-world:1.0.0 pypytesting.azurecr.io/fastapi-hello-world:1.0.0
docker push pypytesting.azurecr.io/fastapi-hello-world -a
```

Create an Azure Container Instance and deploy from the Docker image:

```console
az container create --resource-group pypy-testing --name pypy-fastapi-hello-world --image pypytesting.azurecr.io/fastapi-hello-world:1.0.0 --dns-name-label pypy-fastapi-hello-world --ports 80
az container attach --resource-group pypy-testing --name pypy-fastapi-hello-world
```
