# pylint: disable=no-member
from discord_webhook import DiscordWebhook

from telathbot.config import get_settings
from telathbot.logger import LOGGER


def send_ip_changed_notification(new_ip: str) -> bool:
    config = get_settings()

    webhook = DiscordWebhook(
        url=config.discord_webhook,
        rate_limit_retry=True,
        content=f"TelathBot's Public IP has changed to **{new_ip}**.  Please update database firewall rule in CPanel!",
    )

    response = webhook.execute()

    succeeded = False
    if response.status_code != 200:
        LOGGER.error(
            f"Discord Webhook (Public IP) failed with status code {response.status_code}"
        )
    else:
        LOGGER.info("Discord Webhook (Public IP) succeeded.")
        succeeded = True

    return succeeded
