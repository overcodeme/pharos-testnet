import aiohttp
import random
import asyncio
from utils.logger import logger
from utils.file_manager import load_yaml


settings = load_yaml('./settings.yaml')
SLEEP_DURATION = settings['SLEEP_DURATION']

async def checkin(session: aiohttp.ClientSession, wallet_address, headers):
    url = f'https://api.pharosnetwork.xyz/sign/in?address={wallet_address}'

    async with session.post(url=url, headers=headers) as response:
        if response.status == 200:
            data = await response.text()
            if 'already signed in today' in data:
                logger.warning(wallet_address, f'Already completed checkin today')
                return True
            else:
                logger.success(wallet_address, f'Daily check-in task completed')
                return True
        else:
            random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
            logger.error(wallet_address, f'Error while daily checking in: {response.text()}. Retrying in {random_sleep} sec...')
            await asyncio.sleep(random_sleep)
