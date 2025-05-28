import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Email configuration
gmail_user = 'vuyyala6@gmail.com'
gmail_app_password = 'gpxekuxbssuqwope'
to = 'nageswara@logusims.com'
subject = 'Trivy Scan Report'
body = 'Please find the attached Trivy scan report.'

# Create the email
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to
msg['Subject'] = subject

# Attach the body text
msg.attach(MIMEText(body, 'plain'))

# Attach the report file (use correct filename here)
filename = 'trivy-report.json'
with open(filename, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

# Send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, to, msg.as_string())

print('Email sent!')
