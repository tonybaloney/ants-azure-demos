from pydantic import BaseModel, BaseSettings
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from example_app.db_models import DBLocation, DBUser

User = pydantic_model_creator(DBUser)
Location = pydantic_model_creator(DBLocation)


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Settings(BaseSettings):
    app_insights_connection_string: str
    db_url: str = "sqlite://sample.db"
    verbose_tracing: bool = True
