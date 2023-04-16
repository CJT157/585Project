from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

table_id = "cps585finalproject.stock_data.company_data"

schema = [
    bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("time", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("open_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("high_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("low_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("close_price", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("volume", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("action_pt", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("action_company", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("rating_current", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("pt_current", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("adjusted_pt_current", "FLOAT", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)