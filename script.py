from telethon import TelegramClient, events
from dotenv import load_dotenv
import requests
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv('API_HASH')
channels_monitor = ['starttuition', 'PTHTassignments', 'elitetutorsg', 'tuittysg', 'myqualitytutor_sg', 'CocoAssignments', 'TuitionJob', 'newtuitionassignments', 'TutorSociety']
keywords = ["Programming", "Coding", "Polytechnic", "Poly", "Computing", "University", "Python", "R Programming", "Javascript", "Node", "React", "ReactJS", "Web Development", "HTML", "CSS", "SQL", "Data Structure", "Algorithms"]

bot_token = os.getenv('BOT_TOKEN')
user_id = os.getenv('USER_ID')

client = TelegramClient('channels-monitor', api_id, api_hash)

for handler in logging.root.handlers:
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))

@client.on(events.NewMessage())
async def handler(event):
    sender = await event.get_input_chat()
    if hasattr(sender, 'channel_id') and hasattr(event.chat, 'username'):  # Ensures it's from a channel
        channel = event.chat.username
        logger.info(f'Message received. Channel: {channel}')
        message = event.message.message
        if (channel in channels_monitor):
            logger.info('Channel matched. Checking if matching keyword exists...')
            for keyword in keywords:
                if keyword.lower() in message.lower():
                    logger.info(f'Keyword matched: {keyword}. Sending to bot...')
                    message = f"\n📢 {message}" 
                    logger.info(message)
                    send_bot_notification(message)
                    break

def send_bot_notification(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': user_id,
        'text': f'{message}'
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logger.info('Message sent to bot successfully.')
        if response.status_code != 200:
            logger.warning("⚠️ Failed to send notification:", response.text)
    except Exception as e:
        logger.error("❌ Error sending notification:", str(e))

client.start()
logger.info('Client created successfully')
logger.info("🚀 Listening for messages...")
client.run_until_disconnected()









