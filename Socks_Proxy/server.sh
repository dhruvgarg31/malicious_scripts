#!/bin/bash

# Define color codes for terminal output
PURPLE='\033[0;35m'
RED='\033[0;31m'
BLUE='\033[0;34m'
WHITE='\033[0;37m'
GREEN='\033[0;32m' 
DEFAULT_COLOR='\033[0m'

# Define Squid port
SQUID_PORT=3128

# Output functions for color-coded messages
out() {
    echo -e "$PURPLE$1$DEFAULT_COLOR"
}

info() {
    echo -e "$BLUE$1$DEFAULT_COLOR"
}

white() {
    echo -e "$WHITE$1$DEFAULT_COLOR"
}

success() {
    echo -e "$GREEN$1$DEFAULT_COLOR"
}

error() {
    echo -e "$RED$1$DEFAULT_COLOR"
    exit 1
}

# Install Squid if not already installed
install_squid() {
    INSTALLED=`which squid`
    if [ -z "$INSTALLED" ]; then
        sudo yum update -y > /dev/null
        sudo yum install -y squid > /dev/null
        success '[+] Squid Proxy Installed.'
    else
        info '[~] Squid Proxy already installed.'
    fi
}

# Configure firewall to allow Squid's port
configure_firewall() {
    sudo firewall-cmd --permanent --add-port=$SQUID_PORT/tcp
    sudo firewall-cmd --reload
    success "[+] Squid port $SQUID_PORT is now open."
}

# Fetch external IP
fetch_external_ip() {
    export EXTERNAL_IP=`hostname -I | awk '{print $1}'`
}

# Start Squid proxy service
start_squid() {
    sudo systemctl start squid
    success '[+] Squid Proxy started.'
}

# Stop Squid proxy service
stop_squid() {
    sudo systemctl stop squid
    success '[+] Squid Proxy stopped.'
}

# Check Squid proxy service status
status_squid() {
    sudo systemctl status squid --no-pager
}

# Create Squid user and configure authentication
create_squid_user() {
    USERNAME=$1
    PASSWORD=$2

    if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
        error "[-] ERROR! Username or password not provided."
    fi

    # Create the user if it doesn't exist
    if id "$USERNAME" &>/dev/null; then
        info "[~] User $USERNAME already exists."
    else
        sudo useradd $USERNAME
        echo "$USERNAME:$PASSWORD" | sudo chpasswd
        success "[+] User $USERNAME created successfully."
    fi

    # Create password file for Squid authentication
    sudo htpasswd -b /etc/squid/squid_passwd $USERNAME $PASSWORD
    success "[+] User $USERNAME added to Squid authentication."

    # Enable Squid authentication in Squid configuration
    sudo sed -i 's/#auth_param basic program auth_param basic children 5 auth_param basic realm Squid Proxy auth_param basic credentialsttl 2 hours/auth_param basic program /usr/lib/squid/basic_ncsa_auth \/etc\/squid\/squid_passwd/' /etc/squid/squid.conf
    sudo systemctl restart squid
    success "[+] Squid configured to use authentication."
}

# Set up logging for Squid
configure_squid_logging() {
    sudo sed -i 's/access_log none/access_log /var/log/squid/access.log squid/' /etc/squid/squid.conf
    sudo systemctl restart squid
    success "[+] Squid logging enabled."
}

# Display usage
usage() {
    info "USAGE: $0 [ install | start | stop | status | create-user <username> <password> | configure-logging ]"
    exit 1
}

# Main script execution based on passed arguments
if [ "$#" -lt 1 ]; then
    usage
fi

case $1 in
    install)
        info '[~] Installing Squid Proxy...'
        install_squid
        configure_firewall
        ;;
    start)
        info '[~] Starting Squid Proxy...'
        start_squid
        status_squid
        ;;
    stop)
        info '[~] Stopping Squid Proxy...'
        stop_squid
        status_squid
        ;;
    status)
        status_squid
        ;;
    create-user)
        if [ -z $2 ] || [ -z $3 ]; then
            error "[-] ERROR! Username or password not provided."
        else
            create_squid_user $2 $3
        fi
        ;;
    configure-logging)
        info '[~] Configuring Squid logging...'
        configure_squid_logging
        ;;
    *)
        usage
        ;;
esac
