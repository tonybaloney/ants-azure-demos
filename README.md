# ants-azure-demos

Collection of PoCs and Azure Demos

## Apps

### Django Web App on App Service

[link](https://github.com/tonybaloney/ants-azure-demos/tree/master/django-web-app)

Features

- Azure blob storage for static file
- Django 3 with ASGI
- OpenCensus for monitoring
- Postgres backend

See [pycon-django-workshop](https://github.com/tonybaloney/pycon-django-workshop) for a more modern sample

### FastAPI + App Insights

A demonstration of FastAPI with App Insights for tracing

[link](https://github.com/tonybaloney/ants-azure-demos/tree/master/fastapi-app-insights)

- Devcontainer
- OpenTelemetry exporter for FastAPI to trace events
- Custom exception handler for OpenTelemetry
- Tortoise ORM

### FastAPI + Beanie ODM + Cosmos

A demonstration of Beanie ODM for FastAPI using Cosmos DB as the datastore

[link](https://github.com/tonybaloney/ants-azure-demos/tree/master/fastapi-cosmos-beanie)

Features

- E2E pagination
- API for getting, listing and adding addresses
- Seed API for creating test data using mimesis
- GEO JSON field example for geographic data
- Startup.sh file for Azure App Service

### FastAPI + Cosmos

Minimal example for using the Cosmos Python SDK for CRUD operations on a Cosmos Database with a FastAPI frontend

[link](https://github.com/tonybaloney/ants-azure-demos/tree/master/fastapi-cosmos)
