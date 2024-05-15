import yaml
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def load_last_start_time(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            last_start_time = yaml.safe_load(file)
    except FileNotFoundError:
        last_start_time = None
    return last_start_time

def load_last_end_time(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            last_end_time = yaml.safe_load(file)
    except FileNotFoundError:
        last_end_time = None
    return last_end_time

def save_time_to_yaml(file_path, time):
    with open(file_path, 'w') as file:
        yaml.dump(time, file)

def send_email(sender_email, sender_password, recipientsTO, recipientsCC, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipientsTO)
    msg['CC'] = ", ".join(recipientsCC)  # Join all CC recipients with a comma
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)  
    server.quit()

def main():
    config = load_config('config.yaml')
    recipientsTO = config.get('recipientsTO', [])
    recipientsCC = config.get('recipientsCC', [])
    sender_email = 'EMAIL'
    sender_password = 'PASSWD'
    current_time = datetime.datetime.now().time()

    # Check if current time is between 8:00 and 9:30
    if datetime.time(8, 0) <= current_time <= datetime.time(9, 30):
        # Load last start time from file
        last_start_time = load_last_start_time('last_start.yaml')

        # If last start time is None or not today, send start email
        today = datetime.date.today()
        if last_start_time is None or last_start_time.get('date') != str(today):
            day_of_week = today.strftime('%A')
            email_content = config.get('email_content', {}).get(day_of_week.capitalize(), {}).get('start', '')

            # Prepare subject and message
            subject = f"PF&DPT - praca {today} start"
            message = email_content

            # Send email
            send_email(sender_email, sender_password, recipientsTO, recipientsCC, subject, message)
            print("Start email sent.")

            # Update last start time
            save_time_to_yaml('last_start.yaml', {'date': str(today), 'time': str(datetime.datetime.now())})

    else:
        # Load last end time from file
        last_end_time = load_last_end_time('last_end.yaml')

        # If last end time is None or not today, check if 8h10min have passed since last start time
        today = datetime.date.today()
        if last_end_time is None or last_end_time.get('date') != str(today):
            last_start_time = load_last_start_time('last_start.yaml')
            if last_start_time is not None and last_start_time.get('date') == str(today):
                start_time = datetime.datetime.strptime(last_start_time.get('time'), "%Y-%m-%d %H:%M:%S.%f")
                elapsed_time = datetime.datetime.now() - start_time
                if elapsed_time >= datetime.timedelta(hours=8, minutes=10):
                    # Load email content and send end email
                    day_of_week = today.strftime('%A')
                    email_content = config.get('email_content', {}).get(day_of_week.capitalize(), {}).get('stop', '')

                    # Prepare subject and message
                    subject = f"PF&DPT - praca {today} stop"
                    message = email_content

                    # Send email
                    send_email(sender_email, sender_password, recipientsTO, recipientsCC, subject, message)
                    print("Stop email sent.")

                    # Update last end time
                    save_time_to_yaml('last_end.yaml', {'date': str(today), 'time': str(datetime.datetime.now())})

if __name__ == "__main__":
    main()
