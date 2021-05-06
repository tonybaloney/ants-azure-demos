from typing import Container, Optional, List
import os

from azure.cosmos import CosmosClient
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy
import azure.cosmos.exceptions as exceptions
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

USERPROFILE_CONTAINER = "userprofile"

# Models


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


# Cosmos DB Connection


def get_database() -> DatabaseProxy:
    client = CosmosClient(
        url=os.getenv("COSMOS_URL"), credential=os.getenv("COSMOS_KEY")
    )

    return client.create_database_if_not_exists(os.getenv("COSMOS_DATABASE", "fastapi"))


def get_user_container() -> ContainerProxy:
    try:
        return get_database().get_container_client(USERPROFILE_CONTAINER)
    except exceptions.CosmosResourceNotFoundError:
        return get_database().create_container(USERPROFILE_CONTAINER)


# Helper functions for reading/writing from Cosmos.


def get_user(username: str):
    try:
        result = get_user_container().read_item(item=username, partition_key=username)

        if not result:
            return None
        user = User(**result)
        return user
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except exceptions.CosmosHttpResponseError as cxe:
        raise HTTPException(
            status_code=400, detail="Bad request {0}".format(cxe.http_error_message)
        )


def get_users():
    try:
        result = get_user_container().read_all_items()
        users = [User(**item) for item in result]
        return users
    except exceptions.CosmosHttpResponseError as cxe:
        raise HTTPException(
            status_code=400, detail="Bad request {0}".format(cxe.http_error_message)
        )


def _create_user(user: User):
    try:
        new_user = user.dict()
        new_user["id"] = user.username
        get_user_container().upsert_item()
        return
    except exceptions.CosmosHttpResponseError as cxe:
        raise HTTPException(
            status_code=400, detail="Bad request {0}".format(cxe.http_error_message)
        )


# FastAPI specific code
app = FastAPI()

# API Routes


@app.get("/users/{username}", response_model=User)
async def read_user(username: str):
    user = get_user(username=username)
    return user


@app.get("/users/", response_model=List[User])
async def read_users():
    users = get_users()
    return users


@app.post("/users/")
async def create_user(user: User):
    return _create_user(user=user)
