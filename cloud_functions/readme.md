Cloud Functions

- API Function
    - query stock data from alpaca api
    - query analyst data from analyst api
    - format data to be pushed to bigquery table (will have table schema eventually)

- BigQuery->Storage Function
    - needs to do this https://cloud.google.com/bigquery/docs/samples/bigquery-extract-table-json
    - should be a trigger activated function after previous function finishes