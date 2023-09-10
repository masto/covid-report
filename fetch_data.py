"""Module to get the latest COVID data"""

import logging
import os
import time

import pandas as pd
import pygal
from pygal.style import CleanStyle
from sodapy import Socrata

# https://health.data.ny.gov/resource/jvfi-ffup.csv
_NYS_DATASET_ID = os.environ.get("NYS_DATASET_ID", "jvfi-ffup")
_NYS_FILTER = os.environ.get(
    "NYS_FILTER", "geography_description = 'Nassau' AND geography_level = 'COUNTY'"
)

_CACHE_TIME = 60 * 60  # 1 hour


def get_nys_data():
    """Fetch last 30 days of NYS COVID stats.

    Augmented with cases/100k and rolling 7-day average.
    """

    # Check cache
    now = time.monotonic()
    try:
        if now < get_nys_data.cached_at + _CACHE_TIME:
            logging.warning("get_nys_data() returning from cache")
            return get_nys_data.cached_data
    except AttributeError:
        pass

    with Socrata("health.data.ny.gov", os.environ.get("NYS_APP_TOKEN", None)) as client:
        data = client.get(
            _NYS_DATASET_ID, where=_NYS_FILTER, order="test_date DESC", limit=37
        )

    dataframe = (
        pd.DataFrame.from_records(data)
        .astype(
            {
                "test_date": "datetime64",
                "geography_description": "string",
                "total_new_positives": "int",
                "total_cases_per_100k": "float",
                "total_cases_per_100k_7_day": "float",
            }
        )
        .set_index("test_date")
    )

    get_nys_data.cached_at = now
    get_nys_data.cached_data = {"daily": dataframe}
    return get_nys_data.cached_data


def make_charts(data):
    """Generate pretty chart(s)"""
    chart_style = CleanStyle(background="white")
    chart_7d = pygal.Line(style=chart_style)
    chart_7d.add("", data["daily"][6::-1]["total_cases_per_100k_7_day"].round(1))

    charts = {"cases_per_100k_7day": chart_7d}

    return charts


if __name__ == "__main__":
    df = get_nys_data()
    print(df)
