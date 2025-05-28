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

msg.attach(MIMEBase('application', 'octet-stream'))
msg.attach(MIMEBase('application', 'octet-stream'))
msg.attach(MIMEBase('application', 'octet-stream'))

# Attach the report
filename = 'trivy-report.txt'
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
