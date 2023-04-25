from google.cloud import bigquery

# Connect to Bigquery
client = bigquery.Client(project="cps585finalproject")

dataset_id = "{}.stock_data".format(client.project)

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

dataset.location = "US"

# Send the dataset to the API for creation, with an explicit timeout.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(dataset, timeout=30)
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))