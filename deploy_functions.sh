gcloud auth login
gcloud config set project cps585finalproject

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
