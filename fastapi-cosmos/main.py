from typing import Optional, List
import os

from azure.cosmos import CosmosClient
from azure.cosmos.database import DatabaseProxy
import azure.cosmos.exceptions as exceptions
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


def get_database() -> DatabaseProxy:
    client = CosmosClient(
        url=os.getenv("COSMOS_URL"), credential=os.getenv("COSMOS_KEY")
    )

    return client.create_database_if_not_exists(os.getenv("COSMOS_DATABASE", "fastapi"))


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def get_user(database: DatabaseProxy, username: str):
    try:
        result = database.get_container_client(container="userprofile").read_item(
            item=username, partition_key=username
        )
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    if not result:
        return None
    user = User(**result)
    return user


def get_users(database: DatabaseProxy):
    try:
        result = database.get_container_client(container="userprofile").read_all_items()
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    if not result:
        return None
    users = [User(**item) for item in result]
    return users


# FastAPI specific code
app = FastAPI()


@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    database = get_database()
    user = get_user(database=database, username=username)
    return user


@app.get("/users/", response_model=List[User])
def read_users():
    database = get_database()
    users = get_users(database=database)
    return users
