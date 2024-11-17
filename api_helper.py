import requests
import pandas as pd
import json
import time

# API utility functions
def load_creds():
    """Load credentials from the config.json file."""
    with open('config.json', 'r') as file:
        creds = json.load(file)
    return creds

def getCreds(profile='productminimal'):
    """Retrieve the credentials for the specified profile."""
    creds = load_creds()
    return creds.get(profile, None)

def makeApiCall(url, endpointParams, debug='no'):
    response = requests.get(url, params=endpointParams)
    data = {
        'url': response.url,
        'endpoint_params': endpointParams,
        'json_data': response.json()
    }
    if debug == 'yes':
        print(f"URL: {data['url']}")
        print(f"Response: {data['json_data']}")
    return data

def getInstagramInsights(profile, metric, period=None, metric_type=None, breakdown=None, since=None, until=None, timeframe=None):
    creds = getCreds(profile)
    ig_user_id = creds['instagram_account_id']
    access_token = creds['access_token']
    url = f"{creds['graph_domain']}/{creds['graph_version']}/{ig_user_id}/insights"

    base_params = {
        "metric": metric,
        "access_token": access_token
    }
    if period:
        base_params["period"] = period
    if metric_type:
        base_params["metric_type"] = metric_type
    if since:
        base_params["since"] = since
    if until:
        base_params["until"] = until
    if timeframe:
        base_params["timeframe"] = timeframe
    if breakdown:
        base_params["breakdown"] = breakdown

    response = makeApiCall(url, base_params, creds['debug'])
    return response['json_data']

def json_to_dataframe(data, breakdown_filter=None):
    """
    Converts nested JSON into a tabular DataFrame format.
    Filters by breakdown type if breakdown_filter is specified.
    """
    all_rows = []

    for insight_data in data.get("data", []):
        name = insight_data.get("name", "")
        period = insight_data.get("period", "")
        title = insight_data.get("title", "")
        description = insight_data.get("description", "")
        id_val = insight_data.get("id", "")

        for breakdown_data in insight_data.get("total_value", {}).get("breakdowns", []):
            dimension_key = ", ".join(breakdown_data.get("dimension_keys", []))
            if breakdown_filter and dimension_key != breakdown_filter:
                continue

            for result in breakdown_data.get("results", []):
                dimension_value = ", ".join(result.get("dimension_values", []))
                value = result.get("value", 0)
                # Add row to table
                all_rows.append([name, period, title, description, id_val, dimension_key, dimension_value, value])

    # Create DataFrame
    columns = ["Name", "Period", "Title", "Description", "ID", "Dimension Key", "Dimension Value", "Value"]
    return pd.DataFrame(all_rows, columns=columns)

def process_and_display(profile):
    # Fetch time-series metrics
    time_series_metrics = "reach,impressions"
    since = int(time.time()) - (7 * 24 * 60 * 60)  # Last 7 days
    until = int(time.time())  # Current timestamp

    print(f"\nFetching time-series metrics for {profile.capitalize()}...")
    time_series_data = getInstagramInsights(
        profile=profile,
        metric=time_series_metrics,
        period="day",
        since=since,
        until=until
    )
    df_time_series = json_to_dataframe(time_series_data)
    print(df_time_series)

    # Fetch demographic metrics with breakdowns
    demographic_metrics = "engaged_audience_demographics,reached_audience_demographics"
    breakdowns = ["age", "gender", "city", "country"]

    for breakdown in breakdowns:
        print(f"\nFetching demographic metrics ({breakdown}) for {profile.capitalize()}...")
        demographic_data = getInstagramInsights(
            profile=profile,
            metric=demographic_metrics,
            metric_type="total_value",
            period="lifetime",
            timeframe="this_month",
            breakdown=breakdown
        )
        df_demographics = json_to_dataframe(demographic_data, breakdown_filter=breakdown)
        print(df_demographics)

if __name__ == "__main__":
    process_and_display("productminimal")
    process_and_display("productsdesign")
