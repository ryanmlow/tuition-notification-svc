# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this service does

Monitors a hardcoded list of Singapore tuition Telegram channels for messages matching programming/tech keywords. On a match, forwards the message to a Telegram bot which sends a notification to a specific user.

Uses a **user account** (not a bot account) via Telethon — bots cannot receive channel messages.

## Architecture

AWS Lambda triggered by EventBridge once daily (9 AM SGT / 1 AM UTC). Polls each channel for the last 24 hours of messages, checks keywords, sends notifications via the Telegram Bot API.

Credentials and session are stored in SSM Parameter Store (`/tuition-notifier/*`).

Key files:
- `src/lambda_handler.py` — deployed Lambda function
- `src/requirements.txt` — Lambda dependencies
- `template.yaml` — SAM template (Lambda + EventBridge + IAM)
- `samconfig.toml` — SAM deploy config (region: ap-southeast-1)

## Local development

To invoke locally via SAM (requires AWS credentials with SSM read access):

```sh
sam build && sam local invoke TuitionNotifierFunction
```

## Deployment

Push to `master` triggers `.github/workflows/deploy.yml`, which runs `sam build && sam deploy`.

GitHub Actions secrets required: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.

SAM creates/updates the CloudFormation stack `tuition-notification-svc` in `ap-southeast-1`.

## Key implementation details

- Session is stored as a `StringSession` string in SSM — no file I/O in Lambda
- `iter_messages(channel)` iterates newest-first; loop breaks at the first message older than 24h
- Keyword matching is case-insensitive and breaks on first match to avoid duplicate notifications
- Notifications sent via Telegram Bot API (`requests.post`), not through the Telethon client
- SSM parameter names: `api_id`, `api_hash`, `bot_token`, `user_id`, `session_string` under prefix `/tuition-notifier/`
