# Deployment steps

- Create a resource group
- Create an Application Plan on Linux, P1V2 is ok for production workloads
- Create a web app on Python 3.8
- Set the startup file to a custom startup.sh
- Deploy!

## Deployment via Azure CLI

```console
az group create -l australiaeast -n fastapi-demo
az appservice plan create -g fastapi-demo -n fastapi-plan --is-linux --sku P1V2 --location australiaeast
az webapp create -g fastapi-demo -n fastapi-web -p fastapi-plan --runtime "python|3.8"
az webapp config set --startup-file "startup.sh" -g fastapi-demo -n fastapi-web
```
