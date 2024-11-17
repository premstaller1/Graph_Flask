from flask import Flask, render_template, request, jsonify
from audience_call import getInstagramInsights, json_to_dataframe

app = Flask(__name__)

@app.route('/')
def index():
    """Render the dashboard."""
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    """Fetch Instagram insights and return as JSON."""
    try:
        # Fetch form data
        profile = request.form.get('profile')
        metric = request.form.get('metric')
        breakdown = request.form.get('breakdown')

        # Fetch insights from API
        data = getInstagramInsights(
            profile=profile,
            metric=metric,
            period="lifetime",
            metric_type="total_value",
            breakdown=breakdown
        )

        # Convert API data to DataFrame, then to JSON
        df = json_to_dataframe(data, breakdown_filter=breakdown)
        if df.empty:
            return jsonify({"error": "No data found for the selected parameters."})

        # Return JSON response
        return jsonify(df.to_dict(orient='list'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
