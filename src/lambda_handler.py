import asyncio
import boto3
import logging
import requests
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CHANNELS = [
    'starttuition', 'PTHTassignments', 'elitetutorsg', 'tuittysg',
    'myqualitytutor_sg', 'CocoAssignments', 'TuitionJob',
    'newtuitionassignments', 'TutorSociety',
]
KEYWORDS = [
    "programming",
    "coding",
    "python",
    "javascript",
    "typescript",
    "java",
    "c++",
    "html",
    "css",
    "sql",
    "react",
    "node.js",
    "nodejs",
    "angular",
    "vue",
    "flutter",
    "web development",
    "web dev",
    "software engineering",
    "computer science",
    "data structures",
    "algorithms",
    "machine learning",
    "data science",
    "r programming",
    "computing",
]
SSM_PREFIX = '/tuition-notifier'


def get_params():
    ssm = boto3.client('ssm')
    names = [f'{SSM_PREFIX}/{k}' for k in ('api_id', 'api_hash', 'bot_token', 'user_id', 'session_string')]
    result = ssm.get_parameters(Names=names, WithDecryption=True)
    return {p['Name'].split('/')[-1]: p['Value'] for p in result['Parameters']}


def send_notification(bot_token, user_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    try:
        resp = requests.post(url, data={'chat_id': user_id, 'text': f'\n📢 {message}'})
        if resp.status_code == 200:
            logger.info('Notification sent.')
        else:
            logger.warning(f'Failed to send notification: {resp.text}')
    except Exception as e:
        logger.error(f'Error sending notification: {e}')


async def poll(params):
    client = TelegramClient(
        StringSession(params['session_string']),
        int(params['api_id']),
        params['api_hash'],
    )
    await client.connect()

    since = datetime.now(timezone.utc) - timedelta(hours=24)
    notifications_sent = 0

    for channel in CHANNELS:
        logger.info(f'Checking {channel}...')
        try:
            async for msg in client.iter_messages(channel):
                if msg.date < since:
                    break
                if not msg.text:
                    continue
                for keyword in KEYWORDS:
                    if keyword.lower() in msg.text.lower():
                        logger.info(f'Keyword matched: "{keyword}" in {channel}')
                        send_notification(params['bot_token'], params['user_id'], msg.text)
                        notifications_sent += 1
                        break
        except Exception as e:
            logger.error(f'Error reading {channel}: {e}')

    await client.disconnect()
    logger.info(f'Done. {notifications_sent} notification(s) sent.')


def lambda_handler(event, context):
    params = get_params()
    asyncio.run(poll(params))
    return {'statusCode': 200}
