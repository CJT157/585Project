import functions_framework
from alpaca_trade_api import REST
from benzinga import financial_data
from dotenv import load_dotenv
from google.cloud import bigquery, pubsub_v1, storage
from datetime import datetime
import os, json

@functions_framework.http
def get_stock_data(request):

     """
     Gets stock data from Alpaca and Benzinga APIs and sends it to Bigquery
     Sends a message to a Pub/Sub topic to trigger the next function when done

     Returns:
         string: string indicating success or failure
     """

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
          
          return 'ERROR'

     # Return an HTTP response
     return 'OK'


def table_to_json(data, context):

    """
    Converts data from Bigquery to JSON and uploads to GCS

    Returns:
        string: success message
    """
    
    client_storage = storage.Client(project='cps585finalproject')
    bucket_name = '585_stock_data_bucket'
    bucket = client_storage.get_bucket(bucket_name)

    client_bigquery = bigquery.Client()

    # sql for data
    sql_company = "SELECT * FROM `cps585finalproject.stock_data.company_data`"
    sql_analyst = "SELECT * FROM `cps585finalproject.stock_data.analyst_data` LIMIT 250"

    # query data
    df_company = client_bigquery.query(sql_company).to_dataframe()
    df_analyst = client_bigquery.query(sql_analyst).to_dataframe()

    # remove duplicate companies (we can't delete fresh data from table)
    df_company = df_company.drop_duplicates(subset=['symbol'])

    company_ratings = {}

    # get rating for each company and add to dictionary
    for symbol in df_company['symbol']:
        analyst_comp_list = df_analyst[df_analyst['symbol']==symbol]
        vals = {"sell": 0, "hold": 0, "buy": 0}
        for index, row in analyst_comp_list.iterrows():
            if row['rating_current'] in ["Sell", "Strong Sell"]:
                vals["sell"] += 1.0
            elif row['rating_current'] in ["Underperform", "Underweight", "Moderate Sell", "Weak Hold", "Reduce"]:
                vals["hold"] += .25
                vals["sell"] += .75
            elif row['rating_current'] in ["Market Perform", "Equal-Weight", "Neutral", "Hold"]:
                vals["hold"] += 1.0
            elif row['rating_current'] in ["Outperform", "Overweight", "Moderate Buy", "Add", "Accumulate"]:
                vals["hold"] += .25
                vals["buy"] += .75
            elif row['rating_current'] in ["Buy", "Strong Buy"]:
                vals["buy"] += 1.0
        
        # calculate percentage for each rating
        vals["buy"] = 0 if analyst_comp_list["symbol"].count() == 0 else (vals["buy"] / analyst_comp_list["symbol"].count()) * 100 
        vals["hold"] = 0 if analyst_comp_list["symbol"].count() == 0 else (vals["hold"] / analyst_comp_list["symbol"].count()) * 100
        vals["sell"] = 0 if analyst_comp_list["symbol"].count() == 0 else (vals["sell"] / analyst_comp_list["symbol"].count()) * 100
        
        company_ratings[symbol] = vals

    # format datetime data to string
    df_company['time'] = df_company['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_company.set_index("symbol", inplace=True)
    final_json = df_company.to_dict(orient='index')

    # convert ratings to json format
    for key, val in company_ratings.items():
        final_json[key].update(val)

    # add last updated time
    final_json['last_updated'] = datetime.now()

    # post json file to cloud storage
    json_object = json.dumps(final_json, indent=4)

    blob = bucket.blob('company_data.json')

    blob.upload_from_string(json_object)

    return 'OK'