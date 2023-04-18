from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

table_id_company = "cps585finalproject.stock_data.company_data"
table_id_analyst = "cps585finalproject.stock_data.analyst_data"

schema_company = [
    bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("time", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("open_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("high_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("low_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("close_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("volume", "INTEGER", mode="REQUIRED"),
]

schema_analyst = [
    bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("time", "TIME", mode="REQUIRED"),
    bigquery.SchemaField("action_pt", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("action_company", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("rating_current", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("pt_current", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("adjusted_pt_current", "FLOAT", mode="REQUIRED"),
]

table_company = bigquery.Table(table_id_company, schema=schema_company)
table_company = client.create_table(table_company)  # Make an API request.

table_analyst = bigquery.Table(table_id_analyst, schema=schema_analyst)
table_analyst = client.create_table(table_analyst)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table_company.project, table_company.dataset_id, table_company.table_id)
)
print(
    "Created table {}.{}.{}".format(table_analyst.project, table_analyst.dataset_id, table_analyst.table_id)
)