import functions_framework
from google.cloud import bigquery, storage
import json

@functions_framework.http
def format_table_data(request):
    
    client_storage = storage.Client(project='cps585finalproject')
    bucket_name = '585_stock_data_bucket'
    bucket = client_storage.get_bucket(bucket_name)

    client_bigquery = bigquery.Client()

    # sql for data
    sql_company = "SELECT * FROM `cps585finalproject.stock_data.company_data`"
    sql_analyst = """
    SELECT * FROM `cps585finalproject.stock_data.analyst_data`
    LIMIT 19
    """

    # query data
    df_company = client_bigquery.query(sql_company).to_dataframe()
    df_analyst = client_bigquery.query(sql_analyst).to_dataframe()

    company_ratings = {}

    # get rating for each company and add to dictionary
    for symbol in df_company['symbol']:
        analyst_comp_list = df_analyst[df_analyst['symbol']==symbol]
        vals = {"sell": 0, "hold": 0, "buy": 0}
        for index, row in analyst_comp_list.iterrows():
            rating_real = translate_rating(row['rating_current'])

            # we can adjust the weight of each rating if needed
            if rating_real == "sell":
                vals["sell"] += 1.0
            elif rating_real == "underperform":
                vals["hold"] += .25
                vals["sell"] += .75
            elif rating_real == "hold":
                vals["hold"] += 1.0
            elif rating_real == "outperform":
                vals["hold"] += .25
                vals["buy"] += .75
            elif rating_real == "buy":
                vals["buy"] += 1.0
        
        # calculate percentage for each rating
        vals["buy"] = (vals["buy"] / analyst_comp_list["symbol"].count()) * 100
        vals["hold"] = (vals["hold"] / analyst_comp_list["symbol"].count()) * 100
        vals["sell"] = (vals["sell"] / analyst_comp_list["symbol"].count()) * 100
        
        company_ratings[symbol] = vals

    df_company.set_index("symbol", inplace=True)
    final_json = df_company.to_dict(orient='index')

    for key, val in company_ratings.items():
        final_json[key].update(val)

    json_object = json.dumps(final_json, indent=4)

    blob = bucket.blob('stock_data.json')

    blob.upload_from_string(json_object)

    return 'OK'

def translate_rating(rating):
    if rating in ["Sell", "Strong Sell"]:
        return "sell"
    elif rating in ["Underperform", "Underweight", "Moderate Sell", "Weak Hold", "Reduce"]:
        return "underperform"
    elif rating in ["Market Perform", "Equal-Weight", "Neutral", "Hold"]:
        return "hold"
    elif rating in ["Outperform", "Overweight", "Moderate Buy", "Add", "Accumulate"]:
        return "outperform"
    elif rating in ["Buy", "Strong Buy"]:
        return "buy"