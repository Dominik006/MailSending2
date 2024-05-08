import yaml
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def load_recipients_from_yaml(file_path):
    with open(file_path, 'r') as file:
        recipients = yaml.safe_load(file)
    return recipients

def load_email_content_from_config(file_path, day_of_week):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config[day_of_week]

def send_email(sender_email, sender_password, receiver_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

def main():
    recipients = load_recipients_from_yaml('recipients.yaml')
    today = datetime.date.today()
    day_of_week = today.strftime('%A')
    email_content = load_email_content_from_config('email_content.yaml', day_of_week)

    sender_email = 'your_email@outlook.com'
    sender_password = 'your_password'

    if datetime.datetime.now().time() < datetime.time(8, 0):
        # Send start email between 8:00 and 9:30
        for recipient in recipients:
            subject = f"PF&DPT - praca {today} start"
            message = email_content['start']
            send_email(sender_email, sender_password, recipient, subject, message)
        print("Start email sent.")

    elif datetime.datetime.now().time() > datetime.time(8, 10):
        # Send stop email not earlier than 8 hours and 10 minutes after start email
        for recipient in recipients:
            subject = f"PF&DPT - praca {today} stop"
            message = email_content['stop']
            send_email(sender_email, sender_password, recipient, subject, message)
        print("Stop email sent.")

if __name__ == "__main__":
    main()