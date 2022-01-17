from telathbot import discord
from telathbot.enums import SafetyToolsLevels


def test_ip_changed_notification():
    assert discord.send_ip_changed_notification(new_ip="1.1.1.1")


def test_safetytool_notification():
    assert discord.send_safetytools_notification(
        level=SafetyToolsLevels.RED,
        post_id=29331,
        thread_id=3359,
        position=20,
        post_user="Bob",
        reaction_users=["Foo", "bar"],
    )
