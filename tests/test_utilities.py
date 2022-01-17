import pytest

from telathbot.public_ip import get_ip_address


@pytest.mark.asyncio
async def test_public_ip(event_loop):
    result = await get_ip_address()
    print(result)
