"""
Send an email via Gmail through Scalekit proxy.

Usage: uv run skills/brand-content-agent/scripts/send_email.py --to "creator@email.com" --subject "Collab?" --body "Hey..."

Output: Send result to stdout.
"""

import argparse
import json
import sys
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scalekit_client import actions, USER_IDENTIFIER, GMAIL_CONNECTION_NAME


def send_email(to: str, subject: str, body: str, from_name: str = None) -> dict:
    """Send an email via Gmail through Scalekit proxy."""
    print(f"[Gmail] Sending email to: {to}", file=sys.stderr)
    print(f"[Gmail] Subject: {subject}", file=sys.stderr)

    # Build RFC 2822 message
    message_lines = []
    if from_name:
        message_lines.append(f"From: {from_name}")
    message_lines.append(f"To: {to}")
    message_lines.append(f"Subject: {subject}")
    message_lines.append("Content-Type: text/plain; charset=utf-8")
    message_lines.append("")
    message_lines.append(body)

    raw_message = "\r\n".join(message_lines)
    encoded = base64.urlsafe_b64encode(raw_message.encode()).decode()

    result = actions.request(
        connection_name=GMAIL_CONNECTION_NAME,
        identifier=USER_IDENTIFIER,
        path="/gmail/v1/users/me/messages/send",
        method="POST",
        body={"raw": encoded},
    )
    return result


def main():
    parser = argparse.ArgumentParser(description="Send email via Gmail")
    parser.add_argument("--to", required=True, help="Recipient email")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body (plain text)")
    parser.add_argument("--from-name", help="Sender display name")
    args = parser.parse_args()

    result = send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        from_name=args.from_name,
    )

    print(f"[Gmail] Email sent successfully!", file=sys.stderr)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
