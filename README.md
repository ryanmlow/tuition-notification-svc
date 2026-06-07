# Tuition Notification Service

Monitors Singapore tuition Telegram channels for programming/tech keywords and forwards matches to a Telegram bot.

Runs as an **AWS Lambda** function triggered once daily at 9 AM SGT (1 AM UTC). Uses Telethon in poll mode — fetches the last 24 hours of messages from each channel on each invocation.

## Architecture

```
EventBridge (daily cron) → Lambda → Telegram Bot API
                                  ↑
                          SSM Parameter Store
                          (credentials + session string)
```

## First-time setup

### 1. Export your session to SSM

The Lambda uses a `StringSession` (a serialised string) instead of a `.session` file.
Run this once locally to export your existing session and get the SSM commands:

```sh
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 migrate_session.py
```

Then run the printed `aws ssm put-parameter` commands to store all five parameters:

| SSM path | Value |
|---|---|
| `/tuition-notifier/api_id` | Telegram API ID from https://my.telegram.org |
| `/tuition-notifier/api_hash` | Telegram API hash |
| `/tuition-notifier/bot_token` | Bot token from BotFather |
| `/tuition-notifier/user_id` | Telegram user ID to receive notifications |
| `/tuition-notifier/session_string` | Output from `migrate_session.py` |

> **Important:** Use `--type SecureString` for all parameters. The Lambda IAM role has `ssm:GetParameters` scoped to `/tuition-notifier/*`.

### 2. Add GitHub Actions secrets

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user key with `lambda:UpdateFunctionCode`, `cloudformation:*`, `ssm:GetParameters`, `s3:*` |
| `AWS_SECRET_ACCESS_KEY` | Corresponding secret |

### 3. Deploy

Push to `master` — the workflow runs `sam build && sam deploy` automatically.

On first deploy SAM creates the CloudFormation stack, Lambda function, and EventBridge schedule.

## Local development

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # includes python-dotenv for local .env loading
```

Required `.env` variables: `API_ID`, `API_HASH`, `BOT_TOKEN`, `USER_ID`

To invoke the Lambda handler locally (requires SAM CLI and AWS credentials with SSM access):

```sh
sam build && sam local invoke TuitionNotifierFunction
```

## Key implementation details

- Session stored as a `StringSession` string in SSM — no file I/O needed in Lambda
- Messages are fetched newest-first; iteration stops at the first message older than 24 hours
- Keyword matching is case-insensitive; breaks on first match to avoid duplicate notifications
- `script.py` (legacy) and `migrate_session.py` are local-only tools, not deployed to Lambda
