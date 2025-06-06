import aiohttp
import random
import asyncio
from utils.logger import logger
from main import settings


SLEEP_AFTER_ERROR = settings['SLEEP_AFTER_ERROR']

async def checkin(wallet_address, headers, proxy):
    url = f'https://api.pharosnetwork.xyz/sign/in?address={wallet_address}'
    session = aiohttp.ClientSession()

    async with session.post(url=url, headers=headers, proxy=proxy) as response:
        if response.status == 200:
            logger.success(wallet_address, 'Daily check-in task completed')
            return True
        else:
            random_sleep = random.randint(SLEEP_AFTER_ERROR[0], SLEEP_AFTER_ERROR[1])
            logger.error(wallet_address, f'Error while daily checking in: {response.text()}. Retrying in {random_sleep} sec...')
            await asyncio.sleep(random_sleep)
            return False
