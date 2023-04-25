import functions_framework
from alpaca_trade_api import REST
from benzinga import financial_data
from dotenv import load_dotenv
from google.cloud import bigquery, pubsub_v1
import os

"""
gcloud functions deploy YOUR_FUNCTION_NAME \
[--gen2] \
--region=YOUR_REGION \
--runtime=YOUR_RUNTIME \
--source=YOUR_SOURCE_LOCATION \
--entry-point=YOUR_CODE_ENTRYPOINT \
TRIGGER_FLAGS
"""

@functions_framework.http
def get_stock_data(request):
     load_dotenv()

     # Connect to Alpaca API
     api = REST(os.environ.get('APCA_API_KEY_ID'), os.environ.get('APCA_API_SECRET_KEY'))

     # Connect to Benzinga API
     fin = financial_data.Benzinga(os.environ.get('BENZINGA_API_SECRET_KEY'))

     #list of companies to grab
     companies = ["MSFT","AAPL","DIS","JNJ", "AMX", "AMGN", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "KO", "JPM", "MCD", "MMM", "MRK", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]

     # Request data for these companies from the trade API
     bars = api.get_snapshots(companies)
     ratings = fin.ratings(pagesize=250, company_tickers="MSFT,AAPL,DIS,JNJ,AMX,AMGN,BA,CAT,CSCO,CVX,GS,HD,HON,IBM,INTC,KO,JPM,MCD,MMM,MRK,NKE,PG,TRV,UNH,CRM,VZ,V,WBA,WMT,DIS,DOW")

     ratings_cleaned = []

     # clean up data in case of missing values
     for rating in ratings['ratings']:
          if rating['action_pt'] != "" and rating['action_company'] != "" and rating['rating_current'] != "" and rating['pt_current'] != "" and rating['adjusted_pt_current'] != "":
               ratings_cleaned.append(rating)

     # get bigquery client/table
     client = bigquery.Client()

     table_id_company = bigquery.Table.from_string("cps585finalproject.stock_data.company_data")
     table_id_analyst = bigquery.Table.from_string("cps585finalproject.stock_data.analyst_data")


     # Format data in list for bigquery
     rows_to_insert_company = [{"symbol": symbol, "time": bars[symbol].daily_bar.t.strftime("%Y-%m-%d %T"), "open_price": bars[symbol].daily_bar.o, 
          "high_price": bars[symbol].daily_bar.h, "low_price": bars[symbol].daily_bar.l, 
          "close_price": bars[symbol].daily_bar.c, "volume": bars[symbol].daily_bar.v} for symbol in bars]

     rows_to_insert_analyst = [{"symbol": rating['ticker'], "time": rating['time'], "date": rating['date'], "action_pt": rating['action_pt'], 
          "action_company": rating['action_company'], "rating_current": rating['rating_current'], "pt_current": float(rating['pt_current']), 
          "adjusted_pt_current": float(rating['adjusted_pt_current'])} for rating in ratings_cleaned]


     # Insert data into bigquery
     errors_company = client.insert_rows_json(table_id_company, rows_to_insert_company)  # Make an API request.
     errors_analyst = client.insert_rows_json(table_id_analyst, rows_to_insert_analyst)  # Make an API request.
     if errors_company == [] and errors_analyst == []:
          print("New rows have been added.")

          # create pub sub client
          publisher = pubsub_v1.PublisherClient()
          topic_path = publisher.topic_path("cps585finalproject", "bigquery_to_json")

          # publish message to pubsub
          data_str = f"db updated"
          data = data_str.encode("utf-8")
          future = publisher.publish(topic_path, data)
          
          print(f"pubsub message ({future.result()}) sent")
     else:
          print("Encountered errors while inserting rows: {} {}".format(errors_company, errors_analyst))

     # Return an HTTP response
     return 'OK'
