import logging
import io
import os
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.tablebatch import TableBatch

import azure.functions as func
import pandas


def main(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Name: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
    df = pandas.read_excel(
        io.BytesIO(myblob.read()),
        engine="openpyxl",
        index_col=0,
        true_values=("Y",),
        false_values=("n",),
    )

    table_service = TableService(
        account_name=os.getenv("TABLE_STORAGE_ACCOUNT_NAME"),
        account_key=os.getenv("TABLE_STORAGE_KEY"),
    )
    records = df.to_dict(orient="records")
    batch = TableBatch()
    for record in records:
        entry = record | {"PartitionKey": myblob.name, "RowKey": record["ABN"]}
        batch.insert_entity(entry)

    table_service.commit_batch("ACN", batch)
