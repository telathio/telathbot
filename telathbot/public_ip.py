from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Union

import httpx


async def get_ip_address() -> Union[IPv4Address, IPv6Address]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api64.ipify.org?format=text")

    return ip_address(response.text)
