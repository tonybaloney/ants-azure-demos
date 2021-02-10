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
    if pandas.isna(postcode):
        return ""
    try:
        postcode = int(postcode.replace("o", "0"))
    except ValueError:  # Must be some other junk value
        return ""
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
    postcode_data = pandas.read_csv(
        "https://raw.githubusercontent.com/Elkfox/Australian-Postcode-Data/master/au_postcodes.csv",
        dtype={"postcode": str},
    )

    df = pandas.read_excel(
        io.BytesIO(myblob.read()),
        engine="openpyxl",
        true_values=("Y",),
        false_values=("n"),
    )

    df.dropna(subset=["ABN"], inplace=True)  # Remove entries with no ABN

    df["Town_City"] = df["Town_City"].apply(lambda x: str(x).title())
    df["Reporting_hours___Paid"].fillna(0, inplace=True)
    df["Reporting_hours___Unpaid"].fillna(0, inplace=True)
    df["Reporting_hours___Total"].fillna(0, inplace=True)
    check_columns = (
        "Operates_in_ACT",
        "Operates_in_NSW",
        "Operates_in_NT",
        "Operates_in_QLD",
        "Operates_in_SA",
        "Operates_in_TAS",
        "Operates_in_VIC",
        "Operates_in_WA",
        "Relief_of_poverty_sickness_or_the_needs_of_the_aged",
        "The_advancement_of_education",
        "The_advancement_of_religion",
        "The_provision_of_child_care_services",
        "Other_purposes_beneficial_to_the_community",
        "BASIC_RELIGIOUS",
        "Conducted_Activities",
        "Animal_Protection",
        "Aged_Care_Activities",
        "Civic_and_advocacy_activities",
        "Culture_and_arts",
        "Economic_social_and_community_development",
        "Emergency_Relief",
        "Employment_and_training",
        "Environmental_activities",
        "Grant_making_activities",
        "Higher_education",
        "Hospital_services_and_rehabilitation_activities",
        "Housing_activities",
        "Income_support_and_maintenance",
        "International_activities",
        "Law_and_legal_services",
        "Mental_health_and_crisis_intervention",
        "Political_activities",
        "Primary_and_secondary_education",
        "Religious_activities",
        "Research",
        "Social_services",
        "Sports",
        "Other_Educations",
        "other_health_service_delivery",
        "Other_recreation_and_social_club_activity",
        "Other",
        "Aboriginal_or_TSI",
        "Aged_Persons",
        "Children",
        "Communities_Overseas",
        "Ethnic_Groups",
        "Gay_Lesbian_Bisexual",
        "General_Community_in_Australia",
        "men",
        "Migrants_Refugees_or_Asylum_Seekers",
        "Pre_Post_Release_Offenders",
        "People_with_Chronic_Illness",
        "People_with_Disabilities",
        "People_at_risk_of_homelessness",
        "Unemployed_Persons",
        "Veterans_or_their_families",
        "Victims_of_crime",
        "Victims_of_Disasters",
        "Women",
        "Youth",
        "Other_charities",
        "Other_beneficiaries_not_listed",
        "Reporting_Obligations___ACT",
        "Reporting_Obligations___NSW",
        "Reporting_Obligations___NT",
        "Reporting_Obligations___QLD",
        "Reporting_Obligations___SA",
        "Reporting_Obligations___TAS",
        "Reporting_Obligations___VIC",
        "Reporting_Obligations___WA",
    )
    for col in check_columns:
        df[col].fillna(False, inplace=True)
    df["State"] = df["Postcode"].apply(map_postcode)
    df = pandas.merge(
        df,
        postcode_data,
        left_on=["Postcode", "Town_City"],
        right_on=["postcode", "place_name"],
        how="left",
    ).drop(columns=["postcode", "place_name", "state_name", "state_code", "accuracy"])
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
