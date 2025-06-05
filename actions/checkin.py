import aiohttp
from utils.logger import logger
import asyncio


async def checkin(wallet_address, headers, proxy):
    url = f'https://api.pharosnetwork.xyz/sign/in?address={wallet_address}'
    session = aiohttp.ClientSession()

    async with session.post(url=url, headers=headers, proxy=proxy) as response:
        if response.status == 200:
            logger.success(wallet_address, 'Daily check-in task completed')
            return True
        else:
            logger.error(wallet_address, f'Error while daily checking in: {response.text()}')
            return False
