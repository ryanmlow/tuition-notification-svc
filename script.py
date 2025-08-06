from telethon import TelegramClient, events
from dotenv import load_dotenv
import requests
import os

load_dotenv()
print('Running tuition notification script...')
# Replace these with your values
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv('API_HASH')
channels_monitor = ['starttuition', 'PTHTassignments', 'elitetutorsg', 'tuittysg', 'myqualitytutor_sg', 'CocoAssignments', 'TuitionJob', 'newtuitionassignments', 'TutorSociety']
keywords = ["Programming", "Coding", "Polytechnic", "Poly", "Computing", "University", "Python", "R Programming", "Javascript", "Node", "React", "ReactJS", "Web Development", "HTML", "CSS", "SQL", "Data Structure", "Algorithms"]

bot_token = os.getenv('BOT_TOKEN')
user_id = os.getenv('USER_ID')

client = TelegramClient('multi_channel_monitor', api_id, api_hash)

@client.on(events.NewMessage())
async def handler(event):
    print('in handler')
    sender = await event.get_input_chat()
    print(sender)

    message = event.message.message
    if hasattr(sender, 'channel_id') and hasattr(event.chat, 'username'):  # Ensures it's from a channel
        channel = event.chat.username
        if (channel in channels_monitor):
            print(f'Channel: {channel}')
            for keyword in keywords:
                if keyword.lower() in message.lower():
                    print(f'Keyword matched: {keyword}')
                    message = f"\n📢 {message}" 
                    print(message)
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
        if response.status_code != 200:
            print("⚠️ Failed to send notification:", response.text)
    except Exception as e:
        print("❌ Error sending notification:", str(e))


client.start()
print("🚀 Listening for messages...")
client.run_until_disconnected()



