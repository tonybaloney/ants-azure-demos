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
        true_values=("Y",),
        false_values=("n", "", " ", None),
    )

    table_service = TableService(
        account_name=os.getenv("TABLE_STORAGE_ACCOUNT_NAME"),
        account_key=os.getenv("TABLE_STORAGE_KEY"),
    )

    records = df.to_dict(orient="records")

    # Batch in 100 rows
    for record_batch in (
        records[pos : pos + 100] for pos in range(0, len(records), 100)
    ):
        batch = TableBatch()
        for record in record_batch:
            entry = {
                "PartitionKey": f"ais",
                "RowKey": str(record["ABN"]),
            }
            for k, v in record.items():
                # Create a friendly camel-case key, e.g. Shoe_MAKER___Fox becomes ShoeMakerFox
                entry[k.replace("_", " ").title().replace(" ", "")] = v

            batch.insert_entity(entry)

        table_service.commit_batch("ACN", batch)
