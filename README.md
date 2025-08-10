# Project Documentation

## Project Overview

This project automates the deployment and execution of a Python script (`script.py`) on an AWS EC2 instance using a GitHub Actions workflow (`deploy.yml`). The script listens to messages from specified Telegram channels, scans each message for predefined keywords, and broadcasts matching messages via a Telegram bot.

## File Roles

- **script.py**: The core Python script that sets up a connection to Telegram via Telethon
- **deploy.yml**: The workflow file which automates deployment by initiating an SSH connection to the EC2 instance, pulling the latest changes from the GitHub repository, and running cleanup logic such as removing existing session and log files.

## Session File Handling

To prevent database lock issues, the deployment process checks for an existing Telegram session file using the `fuser` command. If the session file is found to be in use, it is removed to ensures that a fresh session can be created to avoid database lock conflicts.

## Telegram Credentials

**Important:**  
When providing Telegram credentials, **ALWAYS log in with your phone number** to allow the script to listen for channel messages. This is a requirement for the Telegram API to grant the necessary permissions, as bots are not permitted to run such operations.

## Project Environment Variables

- **API_ID**: Your Telegram API ID, required for authenticating with the Telegram API. Obtained from [https://my.telegram.org](https://my.telegram.org)
- **API_HASH**: Your Telegram API hash, also required for authentication. Also obtained from [https://my.telegram.org](https://my.telegram.org)
- **USER_ID**: UserID which the bot should send messages to
- **BOT_TOKEN**: Bot Token obtained from [BotFather](https://t.me/BotFather).

## Project Secrets

- **EC2_HOST**: The public DNS or IP address of the EC2 instance.
- **EC2_SSH_KEY**: The private SSH key used to authenticate with the EC2 instance.

## Deployment and Script Execution Instructions

1. **After each deployment**, SSH into your EC2 instance:
   ```sh
   ssh -i <path-to-key> <EC2_USER>@<EC2_HOST>
   ```
2. **Start the script manually** to provide Telegram credentials and create the session file:
   ```sh
   python3 script.py
   ```
   - Follow the prompts and log in with your **phone number**.
3. **Once the session file is created**, kill the running script (e.g., with `Ctrl+C`).
4. **Restart the script in the background** to enable logging:
   ```sh
   nohup python3 script.py >> "/var/log/user-data.log" 2>&1 &
   ```
   - This will output script logs to the `user-data.log` file for monitoring.
