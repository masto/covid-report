"""E-mail the daily COVID report"""

import base64
import os

from dotenv import load_dotenv
from flask import Flask, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment, Mail, MailSettings, SandBoxMode

import fetch_data

load_dotenv()

data = fetch_data.get_nys_data()

app = Flask(__name__)
with app.app_context():
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
    html = render_template(
        "index.html",
        data=data,
        history_chart_uri="cid:history-chart",
    )

message = Mail(
    from_email=os.environ.get("SG_FROM_EMAIL"),
    to_emails=os.environ.get("SG_TO_EMAILS"),
    subject=f"COVID Report for {data['daily'].iloc[0].name.strftime('%a %b %e, %Y')}",
    html_content=html,
)
message.add_attachment(
    Attachment(
        file_content=base64.b64encode(png).decode("utf-8").replace("\n", ""),
        file_type="image/png",
        file_name="history-chart.png",
        disposition="inline",
        content_id="history-chart",
    )
)


sg = SendGridAPIClient(os.environ.get("SG_API_KEY"))
response = sg.send(message)
print(response.status_code)
print(response.body)
print(response.headers)
