from flask import Flask, render_template, request, jsonify
from api_helper import getInstagramInsights, json_to_dataframe
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Predefined constants
PROFILES = ["productminimal", "productsdesign"]
METRICS = {
    "reach": {"periods": ["day", "week", "days_28"], "breakdown": ["media_product_type", "follow_type"]},
    "impressions": {"periods": ["day", "week", "days_28"], "breakdown": None},
    "follower_count": {"periods": ["day"], "breakdown": None},
    "engaged_audience_demographics": {"periods": ["lifetime"], "breakdown": ["age", "gender", "city", "country"]},
    "reached_audience_demographics": {"periods": ["lifetime"], "breakdown": ["age", "gender", "city", "country"]},
}
BREAKDOWNS = ["media_product_type", "follow_type", "age", "gender", "city", "country"]

TEMPLATES = {
    "Basic Reach": {
        "profile": "productminimal",
        "metric": "reach",
        "period": "day",
        "breakdown": None,
        "since": "2024-11-01",
        "until": "2024-11-07"
    },
    "Advanced Insights": {
        "profile": "productsdesign",
        "metric": "impressions,reach",
        "period": "week",
        "breakdown": "media_product_type",
        "since": "2024-10-01",
        "until": "2024-10-31"
    }
}

@app.route('/')
def index():
    """Render the home page with the form to select metrics and parameters."""
    return render_template(
        'index.html',
        profiles=PROFILES,
        metrics=list(METRICS.keys()),
        breakdowns=BREAKDOWNS,
        templates=TEMPLATES  # Pass as dictionary
    )

@app.route('/fetch', methods=['POST'])
def fetch_data():
    """Fetch Instagram insights based on user input."""
    profile = request.form.get("profile")
    metric = request.form.get("metric")
    period = request.form.get("period")
    since = request.form.get("since")
    until = request.form.get("until")
    breakdown = request.form.get("breakdown")

    # Convert since/until to Unix timestamps
    since_timestamp = int(pd.Timestamp(since).timestamp()) if since else None
    until_timestamp = int(pd.Timestamp(until).timestamp()) if until else None

    # Fetch insights
    data = getInstagramInsights(
        profile=profile,
        metric=metric,
        period=period,
        since=since_timestamp,
        until=until_timestamp,
        breakdown=breakdown
    )

    # Convert JSON response to DataFrame
    df = json_to_dataframe(data, breakdown_filter=breakdown)

    # Visualize data
    if not df.empty:
        fig = px.bar(
            df,
            x="Dimension Value",
            y="Value",
            color="Dimension Key",
            title=f"{metric.capitalize()} Insights",
        )
        graph_html = fig.to_html(full_html=False)
    else:
        graph_html = "<p>No data available for the selected parameters.</p>"

    return render_template('results.html', graph_html=graph_html, table=df.to_html(classes="table table-striped"))

if __name__ == '__main__':
    app.run(debug=True)
