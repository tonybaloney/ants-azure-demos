import logging
import io
import os
from azure.cosmosdb.table.tableservice import TableService
import azure.functions as func
import pandas


def main(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Name: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
    fs = io.BytesIO()
    myblob.readinto(fs.getbuffer())
    df = pandas.read_excel(fs, index_col=0, engine="openpyxl")

    table_service = TableService(
        account_name=os.getenv("TABLE_STORAGE_ACCOUNT_NAME"),
        account_key=os.getenv("TABLE_STORAGE_KEY"),
    )
    records = df.to_dict(orient="records")
    for record in records:
        table_service.insert_entity("ais", record)
