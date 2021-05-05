from typing import Optional
import os

from azure.cosmos import CosmosClient
from azure.cosmos.database import DatabaseProxy
from fastapi import FastAPI
from pydantic import BaseModel


def get_database() -> DatabaseProxy:
    client = CosmosClient(
        url=os.getenv("COSMOS_URL"), credential=os.getenv("COSMOS_KEY")
    )

    return client.create_database_if_not_exists(os.getenv("COSMOS_DATABASE"))


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def get_user(database: DatabaseProxy, username: str):
    result = database.get_container_client(container="userprofile").read_item(
        item={"username": username}
    )
    if not result:
        return None
    user = User(**result)
    return user


# FastAPI specific code
app = FastAPI()


@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    database = get_database()
    user = get_user(database=database, username=username)
    return user
