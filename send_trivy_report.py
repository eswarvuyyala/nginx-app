import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Load credentials from environment variables
gmail_user = os.environ.get("GMAIL_USER")
gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")

# Receiver email (target recipient)
receiver_email = "nageswara@logusims.com"

# Validation to avoid running without creds
if not gmail_user or not gmail_app_password:
    print("❌ Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.")
    exit(1)

# Create the email message
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = receiver_email
msg['Subject'] = "🛡️ Trivy Scan Report for nginx-app"

body = """Hi,

Please find the attached Trivy security scan report.

Regards,
Jenkins
"""
msg.attach(MIMEText(body, 'plain'))

# Attach the Trivy report file
filename = "trivy-report.txt"
try:
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)
except FileNotFoundError:
    print(f"❌ File '{filename}' not found. Please ensure the report file exists.")
    exit(1)

# Send the email via Gmail SMTP server
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, receiver_email, msg.as_string())
    server.quit()
    print("✅ Email sent successfully to", receiver_email)
except Exception as e:
    print("❌ Failed to send email:", e)
