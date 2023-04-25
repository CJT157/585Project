gcloud auth login
gcloud config set project cps585finalproject

python bigquery/create_dataset.py
python bigquery/create_table.py

gcloud storage buckets create gs://585_stock_data_bucket \
--location=us-central1 \
--storage-class=STANDARD \
--project=cps585finalproject

gcloud pubsub topic create bigquery_to_json

gcloud functions deploy get_stock_data \
--region=us-central1 \
--runtime=python38 \
--env-vars-file=.env.yaml \
--source=./cloud_functions \
--entry-point=get_stock_data \
--trigger-http

gcloud functions deploy table_to_json \
--region=us-central1 \
--runtime=python38 \
--source=./cloud_functions \
--entry-point=table_to_json \
--trigger-topic=bigquery_to_json

gcloud scheduler jobs create http Pull-Stock-Data \
    --schedule "0 */1 * * *" \
    --uri "https://us-central1-cps585finalproject.cloudfunctions.net/get_stock_data" \
    --http-method GET