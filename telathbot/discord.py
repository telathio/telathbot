# pylint: disable=no-member
from discord_webhook import DiscordEmbed, DiscordWebhook

from telathbot.config import get_settings
from telathbot.constants import XENFORO_THREAD_PAGE_SIZE
from telathbot.enums import SafetyToolsLevels
from telathbot.logger import LOGGER


def __generate_url(forum_url: str, post_id: int, thread_id: int, position: int) -> str:
    return f"{forum_url}/index.php?threads/{thread_id}/page-{(position // XENFORO_THREAD_PAGE_SIZE) + 1}#post-{post_id}"


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


def send_safetytools_notification(  # pylint: disable=too-many-arguments
    level: SafetyToolsLevels,
    post_id: int,
    thread_id: int,
    position: int,
    post_user: str,
    reaction_users: list[str],
) -> bool:
    config = get_settings()

    webhook = DiscordWebhook(url=config.discord_webhook, rate_limit_retry=True)

    message_config = {
        SafetyToolsLevels.RED: {
            # https://colorcodes.io/red/fire-truck-red-color-codes/
            "color": "CE2029",
            "description": "Red",
        }
    }

    embed = DiscordEmbed(
        title=f'Safetytools Usage ({ message_config[level]["description"] })',
        description=f"[Link]({__generate_url(config.xenforo_base_url, post_id, thread_id, position)})",
        color=message_config[level]["color"],
    )
    embed.add_embed_field(name="Post Author", value=post_user)
    embed.add_embed_field(name="Reaction User(s)", value=", ".join(reaction_users))

    webhook.add_embed(embed)

    response = webhook.execute()

    succeeded = False
    if response.status_code != 200:
        LOGGER.error(
            f"Discord Webhook (Safetytools Notification) failed with status code {response.status_code}"
        )
    else:
        LOGGER.info("Discord Webhook (Safetytools Notification) succeeded.")
        succeeded = True

    return succeeded
