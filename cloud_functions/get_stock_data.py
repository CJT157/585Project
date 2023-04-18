import functions_framework
from alpaca_trade_api import REST
from benzinga import financial_data
from dotenv import load_dotenv
from google.cloud import bigquery
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
  companies = ["MSFT","AAPL","DIS","JNJ"]

  # Request data for these companies from the trade API
  bars = api.get_snapshots(companies)
  ratings = fin.ratings(company_tickers="MSFT,AAPL,DIS,JNJ")

  # Print out data for each company
  for rating in ratings['ratings']:
    print(f"{rating['ticker']} : {rating['action_pt']} | {rating['action_company']} | {rating['rating_current']} | {rating['pt_current']} | {rating['adjusted_pt_current']}")


  # get bigquery client/table
  client = bigquery.Client()

  table_id_company = bigquery.Table.from_string("cps585finalproject.stock_data.company_data")
  table_id_analyst = bigquery.Table.from_string("cps585finalproject.stock_data.analyst_data")


  # Format data in list for bigquery

  rows_to_insert_company = [{"symbol": symbol, "time": bars[symbol].daily_bar.t, "open_price": bars[symbol].daily_bar.o, 
                             "high_price": bars[symbol].daily_bar.h, "low_price": bars[symbol].daily_bar.l, 
                             "close_price": bars[symbol].daily_bar.c, "volume": bars[symbol].daily_bar.v} for symbol in bars]

  rows_to_insert_analyst = [{"symbol": rating['ticker'], "time": rating['time'], "date": rating['date'], "action_pt": rating['action_pt'], 
                             "action_company": rating['action_company'], "rating_current": rating['rating_current'], "pt_current": rating['pt_current'], 
                            "adjusted_pt_current": rating['adjusted_pt_current']} for rating in ratings['ratings']]
  

  # # Insert data into bigquery

  errors = client.insert_rows_json(table_id_company, rows_to_insert_company)  # Make an API request.
  if errors == []:
       print("New rows have been added.")
  else:
       print("Encountered errors while inserting rows: {}".format(errors))

  errors = client.insert_rows_json(table_id_analyst, rows_to_insert_analyst)  # Make an API request.
  if errors == []:
       print("New rows have been added.")
  else:  
       print("Encountered errors while inserting rows: {}".format(errors))

  # Return an HTTP response
  return 'OK'
