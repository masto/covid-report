"""E-mail the daily COVID report"""

import os

from dotenv import load_dotenv
from flask import Flask, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import fetch_data

load_dotenv()

data = fetch_data.get_nys_data()

app = Flask(__name__)
with app.app_context():
    charts = fetch_data.make_charts(data)
    html = render_template(
        "index.html",
        data=data,
        charts=charts,
        render_png_data_uri=fetch_data.render_png_data_uri,
    )

message = Mail(
    from_email=os.environ.get("SG_FROM_EMAIL"),
    to_emails=os.environ.get("SG_TO_EMAILS"),
    subject=f"COVID Report for {data['daily'].iloc[0].name.strftime('%a %b %e, %Y')}",
    html_content=html,
)

sg = SendGridAPIClient(os.environ.get("SG_API_KEY"))
response = sg.send(message)
print(response.status_code)
print(response.body)
print(response.headers)
