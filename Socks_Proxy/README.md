# Squid Proxy Server Management Script
<a target="_blank">
  <img align="right" height="400" width="450" src="https://github.com/dhruvgarg31/malicious_scripts/blob/master/Socks_Proxy/flow%20diagram.webp">
</a>

This Bash script simplifies the management of a Squid proxy server by providing commands to install, configure, and manage the service. It also supports user authentication and logging.

## Features
- **Install Squid Proxy**: Automatically installs the Squid proxy server if not already installed.
- **Start/Stop/Status**: Manage the Squid proxy service easily.
- **Dynamic User Creation**: Add users for authenticated access to the proxy server.
- **Firewall Management**: Automatically opens the necessary ports for Squid (default: 3128).
- **Logging**: Enables access logs for tracking proxy usage.

## Requirements
- A system running a compatible Linux distribution (e.g., CentOS, RHEL, Fedora).
- `firewalld` for firewall management.
- Root or sudo access.

## Script Usage

### 1. Installation
Clone this repository or copy the script file onto your server.

### 2. Make the Script Executable
- Use the below command
  
    ```bash
    chmod +x server.sh

### 3. Run the Script
The script supports the following commands:

| Command                          | Description                                           |
|----------------------------------|-------------------------------------------------------|
| `install`                        | Installs Squid and configures the necessary settings. |
| `start`                          | Starts the Squid proxy service.                       |
| `stop`                           | Stops the Squid proxy service.                        |
| `status`                         | Checks the current status of the Squid proxy service. |
| `create-user <username> <password>` | Creates a user for proxy authentication.           |
| `configure-logging`              | Enables and configures Squid logging.                 |

### 4. Examples
- **Install Squid Proxy**
    ```bash
    ./server.sh install

- **Start Squid Proxy**

    ```bash
    ./server.sh start

- **Stop Squid Proxy**

    ```bash
    ./server.sh stop

- **Check Squid Proxy Status**

    ```bash
    ./server.sh status

- **Create a User for Authentication**

    ```bash
    ./server.sh create-user myuser mypassword

- **Enable Logging**

    ```bash
    ./server.sh configure-logging

## Configuration
- The script assumes Squid's default port is `3128`. If needed, you can modify this port in the script by changing the value of the `SQUID_PORT` variable:

    ```bash
    SQUID_PORT=3128

- The default Squid configuration file is located at:

    ```bash
    /etc/squid/squid.conf

## Authentication Configuration
- User credentials are stored in `/etc/squid/squid_passwd`.
- The script automatically enables basic authentication in Squid.
## Log Files
- Access logs are stored at `/var/log/squid/access.log`.

## Troubleshooting
- **Firewall Issues:** Ensure `firewalld` is installed and running. The script manages the firewall rules automatically.

    ```bash
    sudo systemctl status firewalld

- **Service Issues:** Restart the Squid service if changes are not applied.
    ```bash
    sudo systemctl restart squid

- **Permissions:** Run the script with `sudo` if you encounter permission issues.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/dhruvgarg31/malicious_scripts/blob/master/Socks_Proxy/LICENSE) file for details.
