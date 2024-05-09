import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import time
import datetime
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

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
    config = read_yaml('config.yaml')
    recipients = config['recipients']
    exceptions = config.get('exceptions', [])
    
    while True:
        # Randomize the time to avoid sending emails at the same time every day
        random_hours = random.randint(8, 9)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        random_time = datetime.time(random_hours, random_minutes, random_seconds)
        random_wait = datetime.datetime.combine(datetime.date.today(), random_time) - datetime.datetime.now()
        if random_wait.total_seconds() > 0:
            time.sleep(random_wait.total_seconds())

        now = datetime.datetime.now()
        if now.hour == random_hours and now.minute < 30:
            start_content = config['start_content']
            send_email('Start pracy', start_content, recipients)
            
            # Wait until at least 8 hours and 10 minutes before sending end email
            time.sleep(29400)  # 8 hours and 10 minutes in seconds
            
            # Check if today is not in exceptions
            if now.strftime('%Y-%m-%d') not in exceptions:
                day_of_week = now.strftime('%A').lower()
                end_content = config.get('end_content', {}).get(day_of_week, '')
                send_email('Koniec pracy', end_content, recipients)

if __name__ == "__main__":
    main()