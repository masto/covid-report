"""Module to get the latest COVID data"""

import pandas as pd
import pygal
from pygal.style import CleanStyle
from sodapy import Socrata

# https://health.data.ny.gov/resource/xdss-u53e.csv
NYS_DATASET_ID = "xdss-u53e"
# https://health.data.ny.gov/Health/New-York-State-Population-Data-Beginning-2003/e9uj-s3sf
NASSAU_POPULATION = 1356924


def get_nys_data():
    """Fetch last 30 days of Nassau County COVID stats.

    Augmented with cases/100k and rolling 7-day average.
    """
    with Socrata("health.data.ny.gov", None) as client:
        data = client.get(
            NYS_DATASET_ID, where="county = 'Nassau'", order="test_date DESC", limit=37
        )

    dataframe = (
        pd.DataFrame.from_records(data)
        .astype(
            {
                "test_date": "datetime64",
                "county": "string",
                "geography": "string",
                "new_positives": "int",
                "cumulative_number_of_positives": "int",
                "total_number_of_tests": "int",
                "cumulative_number_of_tests": "int",
                "test_positive": "string",
            }
        )
        .set_index("test_date")
        .assign(
            cases_per_100k=lambda df: df["new_positives"] / (NASSAU_POPULATION / 100000)
        )
        .assign(
            cases_per_100k_7d=lambda df: df["cases_per_100k"]
            .rolling(window="7D")
            .mean()
            .shift(-6)
        )
    )

    return {"daily": dataframe}


def make_charts(data):
    """Generate pretty chart(s)"""
    chart_7d = pygal.Line(style=CleanStyle)
    chart_7d.add("", data["daily"][6::-1]["cases_per_100k_7d"])

    charts = {"cases_per_100k_7day": chart_7d}

    return charts


if __name__ == "__main__":
    df = get_nys_data()
    print(df)
