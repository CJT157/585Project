import functions_framework

"""
gcloud functions deploy YOUR_FUNCTION_NAME \
[--gen2] \
--region=YOUR_REGION \
--runtime=YOUR_RUNTIME \
--source=YOUR_SOURCE_LOCATION \
--entry-point=YOUR_CODE_ENTRYPOINT \
TRIGGER_FLAGS
"""

# Register an HTTP function with the Functions Framework
@functions_framework.http
def get_stock_data(request):
  # Your code here
  #api = REST(settings.APCA_API_KEY_ID, settings.APCA_API_SECRET_KEY)

  # Fetch all companies from the database
  companies = [] #list of companies to grab

  # Request data for these companies from the trade API
  #snapshots = api.get_snapshots(companies)

  # Return an HTTP response
  return 'OK'