import functions_framework
from alpaca_trade_api import REST
from benzinga import financial_data
from dotenv import load_dotenv
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
  bars = api.get_bars(companies)
  ratings = fin.ratings(company_tickers="MSFT,AAPL,DIS,JNJ")

  for rating in ratings['ratings']:
    print(f"{rating['ticker']} : {rating['action_pt']} | {rating['action_company']} | {rating['rating_current']} | {rating['pt_current']} | {rating['adjusted_pt_current']}")


  # Return an HTTP response
  return 'OK'