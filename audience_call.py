import pandas as pd
from check_update import getCreds, makeApiCall  # Ensure these are correctly imported

def getInstagramInsights(profile, metric, period, metric_type, breakdown=None, timeframe=None, since=None, until=None):
    creds = getCreds(profile)
    ig_user_id = creds['instagram_account_id']
    access_token = creds['access_token']
    url = f"https://graph.facebook.com/v20.0/{ig_user_id}/insights"

    all_results = []

    base_params = {
        "metric": metric,
        "period": period,
        "metric_type": metric_type,
        "access_token": access_token
    }

    if timeframe:
        base_params["timeframe"] = timeframe
    if since:
        base_params["since"] = since
    if until:
        base_params["until"] = until

    if breakdown:
        for element in breakdown.split(','):
            params = base_params.copy()
            params["breakdown"] = element.strip()
            response = makeApiCall(url, params)

            if response.get('json_data'):
                all_results.append({
                    "breakdown": element,
                    "data": response['json_data']
                })
            else:
                all_results.append({
                    "breakdown": element,
                    "error": response
                })
    else:
        response = makeApiCall(url, base_params)
        if response.get('json_data'):
            all_results.append(response['json_data'])
        else:
            all_results.append({"error": response})

    return all_results

def json_to_dataframe(data, breakdown_filter=None):
    """
    Converts nested JSON into a tabular DataFrame format.
    Filters by breakdown type if breakdown_filter is specified.
    """
    all_rows = []

    for item in data:
        breakdown = item.get("breakdown", "")
        if breakdown_filter and breakdown != breakdown_filter:
            continue  # Skip if filtering and this item doesn't match
        
        for insight_data in item.get("data", {}).get("data", []):
            name = insight_data.get("name", "")
            period = insight_data.get("period", "")
            title = insight_data.get("title", "")
            description = insight_data.get("description", "")
            id_val = insight_data.get("id", "")
            for breakdown_data in insight_data.get("total_value", {}).get("breakdowns", []):
                dimension_key = ", ".join(breakdown_data.get("dimension_keys", []))
                for result in breakdown_data.get("results", []):
                    dimension_value = ", ".join(result.get("dimension_values", []))
                    value = result.get("value", 0)
                    # Add row to table
                    all_rows.append([breakdown, name, period, title, description, id_val, dimension_key, dimension_value, value])

    # Create DataFrame
    columns = ["Breakdown", "Name", "Period", "Title", "Description", "ID", "Dimension Key", "Dimension Value", "Value"]
    df = pd.DataFrame(all_rows, columns=columns)
    return df

# Function to fetch, process, and display tables by profile and breakdown type
def process_and_display(profile):
    demographics_metrics = getInstagramInsights(
        profile=profile,
        metric="engaged_audience_demographics,reached_audience_demographics,follower_demographics",
        period="lifetime",
        metric_type="total_value",
        breakdown="age,gender,city,country",
        timeframe="this_month"
    )

    # List of breakdowns to process separately
    breakdowns = ["age", "gender", "city", "country"]

    for breakdown in breakdowns:
        df = json_to_dataframe(demographics_metrics, breakdown_filter=breakdown)
        print(f"{profile.capitalize()} - {breakdown.capitalize()} Demographics Metrics (Tabular Format):")
        print(df)
        print("\n")

# Process and display for each profile
process_and_display("productminimal")
process_and_display("productsdesign")
