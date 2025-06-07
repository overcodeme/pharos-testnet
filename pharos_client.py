from eth_account import Account
from eth_account.messages import encode_defunct
from data.const import pharos_headers, stables_faucet_data
from utils.logger import logger
from utils.file_manager import load_yaml, load_txt
from actions.checkin import checkin
from actions.faucet import fetch_native_faucet, fetch_stable_faucet, is_able_to_faucet
import aiohttp
import asyncio
import random

discords = load_txt('data/discord_tokens.txt')
twitters = load_txt('data/twitter_tokens.txt')
settings = load_yaml('settings.yaml')
ATTEMPTS, SLEEP_BETWEEN_ACTIONS, SLEEP_AFTER_ERROR = settings['ATTEMPTS'], settings['SLEEP_BETWEEN_ACTIONS'], settings['SLEEP_AFTER_ERROR']

class PharosClient:
    def __init__(self, private_key, proxy):
        self.wallet = Account.from_key(private_key)
        self.session = aiohttp.ClientSession(proxy=proxy)
        self.headers = pharos_headers


    def _sign_message(self):
        encoded_message = encode_defunct(text='pharos')
        signature = self.wallet.sign_message(encoded_message)
        return f'0x{signature.signature.hex()}'


    async def login(self):
        url = f'https://api.pharosnetwork.xyz/user/login?address={self.wallet.address}&signature={self._sign_message()}'

        for retry in range(ATTEMPTS):
            try:
                async with self.session.post(url=url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.success(self.wallet.address, 'Successfully logged in')
                        self.headers['authorization'] = f'Bearer {data['data']['jwt']}'
                        return
                    else:
                        random_sleep = random.randint(SLEEP_AFTER_ERROR[0], SLEEP_AFTER_ERROR[1])
                        logger.error(self.wallet.address, f'Error while logging in: {response.text()}. Retrying in {random_sleep} sec...')
                        await asyncio.sleep(random_sleep)
            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred: {e}')


    async def get_user_data(self):
        url = f'https://api.pharosnetwork.xyz/user/profile?address={self.wallet.address}'

        for retry in range(ATTEMPTS):
            try:
                async with self.session.get(url=url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        random_sleep = random.randint(SLEEP_AFTER_ERROR[0], SLEEP_AFTER_ERROR[1])
                        logger.error(self.wallet.address, f'Error while getting user data: {await response.text()} Retrying in {random_sleep} sec...')
                        await asyncio.sleep(random_sleep)

            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred: {e}')
            

    async def fetch_faucet(self):
        user_data = await self.get_user_data()
        stables = stables_faucet_data
        is_twitter_connected = True if user_data['data']['user_info']['XId'] else False
        
        for retry in range(ATTEMPTS):
            try:
                if await is_able_to_faucet(self.session, self.wallet.address, self.headers):
                    await fetch_native_faucet(self.session, self.wallet.address, is_twitter_connected, self.headers)
                    break
            except Exception as e:
                random_sleep = random.randint(SLEEP_AFTER_ERROR[0], SLEEP_AFTER_ERROR[1])
                logger.error(self.wallet.address, f'An error occurred: {e}. Retrying in {random_sleep} sec...')
                await asyncio.sleep(random_sleep)

        for stable in stables:
            for retry in range(ATTEMPTS):
                try:
                    await fetch_stable_faucet(self.wallet.address, stable)
                    break
                except Exception as e:
                    random_sleep = random.randint(SLEEP_AFTER_ERROR[0], SLEEP_AFTER_ERROR[1])
                    logger.error(self.wallet.address, f'An error occurred: {e}. Retrying in {random_sleep} sec...')
                    await asyncio.sleep(random_sleep)


    async def check_in(self):
        for retry in range(ATTEMPTS):
            if await checkin(self.wallet.address, self.headers):
                break


    async def run_onchain(self):
        pass


    async def connect_socials(self):
        pass
                
