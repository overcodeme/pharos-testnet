from eth_account import Account
from eth_account.messages import encode_defunct
from data.const import pharos_headers, stables_data
from utils.logger import logger
from utils.file_manager import load_yaml, load_txt
from actions.checkin import checkin
from actions.faucet import fetch_native_faucet, fetch_stable_faucet, is_able_to_faucet
from actions.onchain_tasks import handle_random_swap, send_to_friends
from colorama import Fore, Style
import aiohttp
import asyncio
import random


discords = load_txt('data/discord_tokens.txt')
twitters = load_txt('data/twitter_tokens.txt')
settings = load_yaml('settings.yaml')
ATTEMPTS, SLEEP_DURATION = settings['ATTEMPTS'], settings['SLEEP_DURATION']
tasks = settings['TASKS']
tasks_functions = {
    'SWAP': handle_random_swap,
    'LIQUIDITY': '',
    'SEND_TO_FRIENDS': send_to_friends,
}


class PharosClient:
    def __init__(self, private_key, proxy=None):
        self.wallet = Account.from_key(private_key)
        self.session = aiohttp.ClientSession(proxy=proxy)
        self.headers = pharos_headers


    def _sign_message(self):
        encoded_message = encode_defunct(text='pharos')
        signature = self.wallet.sign_message(encoded_message)
        return f'0x{signature.signature.hex()}'


    async def login(self):
        url = f'https://api.pharosnetwork.xyz/user/login?address={self.wallet.address}&signature={self._sign_message()}'
        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
        logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before starting...')
        await asyncio.sleep(random_sleep)
        for retry in range(ATTEMPTS):
            try:
                async with self.session.post(url=url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.headers['authorization'] = f'Bearer {data['data']['jwt']}'
                        user_data = await self.get_user_data()
                        logger.info(self.wallet.address, f'Total points: {Fore.YELLOW}{user_data['data']['user_info']['TotalPoints']}{Style.RESET_ALL}')
                        return
                    else:
                        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                        logger.error(self.wallet.address, f'Error while logging in: {response.text()}. Retrying in {random_sleep} sec...')
                        await asyncio.sleep(random_sleep)
            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred while logging in: {e}')


    async def get_user_data(self):
        url = f'https://api.pharosnetwork.xyz/user/profile?address={self.wallet.address}'

        for retry in range(ATTEMPTS):
            try:
                async with self.session.get(url=url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                        logger.error(self.wallet.address, f'Error while getting user data: {await response.text()} Retrying in {random_sleep} sec...')
                        await asyncio.sleep(random_sleep)

            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred while gettings user data: {e}')
            

    async def fetch_faucet(self):
        user_data = await self.get_user_data()
        stables = stables_data
        is_twitter_connected = True if user_data['data']['user_info']['XId'] else False
        
        for retry in range(ATTEMPTS):
            try:
                if await is_able_to_faucet(self.session, self.wallet.address, self.headers):
                    await fetch_native_faucet(self.session, self.wallet.address, is_twitter_connected, self.headers)
                    break
                else:
                    logger.warning(self.wallet.address, 'You already used native faucet today')
                    break
            except Exception as e:
                random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                logger.error(self.wallet.address, f'An error occurred while fetching native faucet: {e}. Retrying in {random_sleep} sec...')
                await asyncio.sleep(random_sleep)

        for stable in stables:
            for retry in range(ATTEMPTS):
                try:
                    await fetch_stable_faucet(self.session, self.wallet, stable['contract_address'])
                    break
                except Exception as e:
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    logger.error(self.wallet.address, f'An error occurred while fetching stable faucet: {e}. Retrying in {random_sleep} sec...')
                    await asyncio.sleep(random_sleep)


    async def check_in(self):
        for retry in range(ATTEMPTS):
            if await checkin(self.session, self.wallet.address, self.headers):
                break


    async def run_onchain(self):
        all_tasks = []
        
        for task_name, task_data in tasks.items():
            task_count = random.randint(task_data.TASK_COUNT[0], task_data.TASK_COUNT[1])
            all_tasks.append({task_name: task_count})
        
        random.shuffle(all_tasks)

        for task in all_tasks:
            for task_name, task_count in task.items():
                for i in range(task_count):
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    await tasks_functions[task_name]()
                    logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before next action...')
                    await asyncio.sleep(random_sleep)


    async def connect_socials(self):
        pass
                

    async def close_session(self):
        if self.session:
            await self.session.close()