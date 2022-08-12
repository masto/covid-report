"""A trivial web app to see everything working"""

import os

from flask import Flask, render_template

import fetch_data

app = Flask(__name__)


@app.route("/")
def index_page():
    """Serve the report up as a web page."""
    data = fetch_data.get_nys_data()
    charts = fetch_data.make_charts(data)

    return render_template(
        "index.html",
        data=data,
        charts=charts,
        render_png_data_uri=fetch_data.render_png_data_uri,
    )


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "5000")
    app.run(debug=False, port=server_port, host="0.0.0.0")
