"""A trivial web app to see everything working"""

import base64
import os

from flask import Flask, render_template

import fetch_data

app = Flask(__name__)


def png_to_data_uri(png):
    """Create a data: URI for a PNG image."""
    return "data:image/png;charset=utf-8;base64,%s" % (
        base64.b64encode(png).decode("utf-8").replace("\n", "")
    )


@app.route("/")
def index_page():
    """Serve the report up as a web page."""
    data = fetch_data.get_nys_data()
    charts = fetch_data.make_charts(data)
    png = charts["cases_per_100k_7day"].render_to_png(
        show_legend=False,
        explicit_size=True,
        height=100,
        width=400,
        margin=2,
        max_scale=5,
        order_min=0.1,
        y_labels_major=[0],
    )

    return render_template(
        "index.html",
        data=data,
        history_chart_uri=png_to_data_uri(png),
    )


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "5000")
    app.run(debug=False, port=server_port, host="0.0.0.0")
