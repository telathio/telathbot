from telathbot import discord


def test_ip_changed_notification():
    assert discord.send_ip_changed_notification(new_ip="1.1.1.1")
