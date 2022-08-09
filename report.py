"""E-mail the daily COVID report"""

import os

from flask import Flask, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import fetch_data

data = fetch_data.get_nys_data()

app = Flask(__name__)
with app.app_context():
    html = render_template("index.html", data=data, today=data.iloc[0])

message = Mail(
    from_email=os.environ.get("SG_FROM_EMAIL"),
    to_emails=os.environ.get("SG_TO_EMAILS"),
    subject=f"COVID Report for {data.iloc[0].name.strftime('%a %b %e, %Y')}",
    html_content=html,
)

sg = SendGridAPIClient(os.environ.get("SG_API_KEY"))
response = sg.send(message)
print(response.status_code)
print(response.body)
print(response.headers)
