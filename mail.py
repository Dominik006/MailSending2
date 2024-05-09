import random
import time
import datetime
import yaml
import win32com.client as win32

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def send_email(subject, body, recipients):
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.Body = body
    mail.To = ';'.join(recipients)
    mail.Send()

def main():
    config = read_yaml('config.yaml')
    recipients = config['recipients']
    exceptions = config.get('exceptions', [])
    
    while True:
        # Randomize the time to avoid sending emails at the same time every day
        random_hours = random.randint(8, 9)
        random_minutes = random.randint(0, 59)
        # Ensure that the random time is between 8:00 and 9:30
        if random_hours == 9:
            random_minutes = random.randint(0, 29)
        random_seconds = random.randint(0, 59)
        random_time = datetime.time(random_hours, random_minutes, random_seconds)
        random_wait = datetime.datetime.combine(datetime.date.today(), random_time) - datetime.datetime.now()
        if random_wait.total_seconds() > 0:
            time.sleep(random_wait.total_seconds())

        now = datetime.datetime.now()
        # Check if the current time is between 8:00 and 9:30
        if 8 <= now.hour < 10 or (now.hour == 9 and now.minute < 30):
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