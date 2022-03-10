from pydantic import BaseModel, BaseSettings
from tortoise.contrib.pydantic import pydantic_model_creator

from .db_models import DBLocation, DBUser

User = pydantic_model_creator(DBUser)
Location = pydantic_model_creator(DBLocation)


class LocationCreate(BaseModel):

    name: str
    private: bool = False


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Settings(BaseSettings):
    db_url: str = "sqlite://sample.db"
    profiling_interval: float = 0.0001
    profiling: bool = True
