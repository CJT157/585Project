import functions_framework
from alpaca_trade_api import REST
from benzinga import financial_data

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
  
  # Connect to Alpaca API
  #api = REST(settings.APCA_API_KEY_ID, settings.APCA_API_SECRET_KEY)

  # Connect to Benzinga API
  #api_key = ""
  #fin = financial_data.Benzinga(api_key)

  #list of companies to grab
  companies = []


  # Request data for these companies from the trade API
  #bars = api.get_bars(companies)
  #fin.ratings("AAPL")


  # Return an HTTP response
  return 'OK'