from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# CORS origins
origins = [
    "*",
]

from .models import Settings

settings = Settings()
app = FastAPI(
    description="Simple API",
    version="1.0.0",
    title="Simple API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routes  # NOQA


@app.on_event("startup")
async def startup_event():
    pass 