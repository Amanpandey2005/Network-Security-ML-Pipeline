import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Sender Email
EMAIL_ADDRESS = "jpamanpandey@gmail.com"

# App Password
EMAIL_PASSWORD = "mlbe piby srsi tuaa"

# Receiver Email
RECEIVER_EMAIL = "amanpandey.code@gmail.com"


def send_alert(
    prediction,
    packet_info,
    receiver_email
):

    try:

        subject = f"⚠ Network Threat Detected: {prediction}"

        body = f"""
Threat Detected!

Attack Type: {prediction}

Packet Information:
{packet_info}

Please check your network immediately.
"""

        msg = MIMEMultipart()

        msg["From"] = EMAIL_ADDRESS

        msg["To"] = RECEIVER_EMAIL

        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Gmail SMTP
        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            RECEIVER_EMAIL,
            msg.as_string()
        )

        server.quit()

        print("✅ Email Alert Sent")

    except Exception as e:

        print("Email Error:", e)