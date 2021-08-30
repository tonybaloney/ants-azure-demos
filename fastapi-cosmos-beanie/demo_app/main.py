import motor
from beanie import init_beanie
from fastapi import FastAPI

from demo_app.models import Settings, __beanie_models__

settings = Settings(_env_file=".env")
app = FastAPI()

from demo_app.routes import address_router


@app.on_event("startup")
async def startup_event():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_connection)
    await init_beanie(
        database=client[settings.mongo_db], document_models=__beanie_models__
    )
    app.include_router(address_router, prefix="/address", tags=["address"])
