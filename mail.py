import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import time
import datetime

def read_email_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    recipients = [line.strip() for line in data]
    return recipients

def read_email_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def read_exceptions(file_path):
    with open(file_path, 'r') as file:
        exceptions = [line.strip() for line in file.readlines()]
    return exceptions

def send_email(subject, body, recipients):
    from_email = 'your_email@example.com'
    to_email = ', '.join(recipients)
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(from_email, 'your_password')
    server.sendmail(from_email, recipients, msg.as_string())
    server.quit()

def main():
    recipients = read_email_data('recipients.txt')
    exceptions = read_exceptions('exceptions.txt')
    
    while True:
        # Randomize the time to avoid sending emails at the same time every day
        random_seconds = random.randint(0, 1800)
        time.sleep(random_seconds)

        now = datetime.datetime.now()
        if now.hour == 8 and now.minute < 30:
            start_content = read_email_content('start_content.txt')
            send_email('Start pracy', start_content, recipients)
            
            # Wait until at least 8 hours and 10 minutes before sending end email
            time.sleep(29400)  # 8 hours and 10 minutes in seconds
            
            # Check if today is not in exceptions
            if now.strftime('%Y-%m-%d') not in exceptions:
                # Determine the filename based on the day of the week
                day_of_week = now.strftime('%A').lower()
                end_content = read_email_content(f'{day_of_week}_end.txt')
                send_email('Koniec pracy', end_content, recipients)

if __name__ == "__main__":
    main()