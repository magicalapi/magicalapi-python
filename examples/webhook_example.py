"""
Example: Using webhook_url for asynchronous response delivery

IMPORTANT: Before using webhooks, you must register your webhook domain
in the whitelist via the MagicalAPI panel: https://panel.magicalapi.com/

For complete setup guide: https://docs.magicalapi.com/docs/webhook
"""

import asyncio

from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import WebhookCreatedResponse


async def main():
    """Example of using webhook URL with resume parser service."""

    # Your webhook endpoint (must be whitelisted in MagicalAPI panel)
    webhook_url = "https://your-domain.com/webhook/magical-api"

    async with AsyncClient(webhook_url=webhook_url) as client:
        # Make a request - the full response will be sent to your webhook_url
        response = await client.resume_parser.get_resume_parser(
            url="https://pub-4aa6fc29899047be8d4a342594b2c033.r2.dev/00016-poduct-manager-resume-example.pdf"
        )

        # With webhook_url, you get an immediate acknowledgment
        if isinstance(response, WebhookCreatedResponse):
            print(f"✅ Request accepted! Status: {response.data.status}")
            print(f"The full response will be sent to: {webhook_url}")
            print(f"Credits: {response.usage.credits}")

        # Handle errors (e.g., domain not whitelisted)
        elif isinstance(response, ErrorResponse):
            if response.status_code == 403:
                print(f"❌ Error: {response.message}")
                print("Register your domain at: https://panel.magicalapi.com/")
            else:
                print(f"Error {response.status_code}: {response.message}")


if __name__ == "__main__":
    asyncio.run(main())
