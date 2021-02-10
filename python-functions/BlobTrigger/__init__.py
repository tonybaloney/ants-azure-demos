import logging
import io
import os
import re
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.tablebatch import TableBatch

import azure.functions as func
import pandas


def camelKey(k):
    """Create a friendly camel-case key, e.g. Shoe_MAKER___Fox becomes ShoeMakerFox"""
    camelKey = k.replace("_", " ").title().replace(" ", "")

    # Remove all the characters that are not allowed in table storage as property names
    return re.sub("\ |\?|\.|\!|\/|\;|\:|\(|\)", "", camelKey)


def map_postcode(postcode):
    postcode = int(postcode)
    if (
        (1000 <= postcode <= 1999)
        or (2000 <= postcode <= 2599)
        or (2619 <= postcode <= 2899)
        or (2921 <= postcode <= 2999)
    ):
        return "NSW"
    if (
        (200 <= postcode <= 299)
        or (2600 <= postcode <= 2618)
        or (2900 <= postcode <= 2920)
    ):
        return "ACT"
    if (3000 <= postcode <= 3999) or (8000 <= postcode <= 8999):
        return "VIC"
    if (4000 <= postcode <= 4999) or (9000 <= postcode <= 9999):
        return "QLD"
    if 5000 <= postcode <= 5999:
        return "SA"
    if 6000 <= postcode <= 6999:
        return "WA"
    if 7000 <= postcode <= 7999:
        return "TAS"
    if 800 <= postcode <= 999:
        return "NT"


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
        false_values=("n"),
    )

    df.dropna(subset=["ABN"], inplace=True)  # Remove entries with no ABN

    df["Town_City"] = df["Town_City"].apply(
        lambda x: str(x).title()
    )  # Title case all city names
    df["Reporting_hours___Paid"].fillna(
        0, inplace=True
    )  # Replace empty reporting hours with zero
    df["Reporting_hours___Unpaid"].fillna(0, inplace=True)
    df["Reporting_hours___Total"].fillna(0, inplace=True)

    df["State"] = df["Postcode"].apply(map_postcode)  # Calculate the postcode

    # Connect to Azure Table Store
    table_service = TableService(
        account_name=os.getenv("TABLE_STORAGE_ACCOUNT_NAME"),
        account_key=os.getenv("TABLE_STORAGE_KEY"),
    )

    # Convert dataframe to list of dictionary
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
                cleanCamelKey = camelKey(k)
                # Check that removing those characters didn't create a duplicate key
                if cleanCamelKey in entry:
                    raise ValueError(f"Key collision on {cleanCamelKey}")

                entry[cleanCamelKey] = v

            batch.insert_or_replace_entity(entry)

        table_service.commit_batch("ACN", batch)
