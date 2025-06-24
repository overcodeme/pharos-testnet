from eth_account import Account
from eth_account.messages import encode_defunct
from data.const import pharos_headers, stables_data
from utils.logger import logger
from utils.file_manager import load_yaml, load_txt
from utils.utils import sign_message
from actions.checkin import checkin
from actions.faucet import fetch_native_faucet, fetch_stable_faucet, is_able_to_faucet
from actions.send_to_friends import handle_send_to_friends_task
from actions.swap import handle_swap
from actions.liquidity import handle_liquidity
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
    'SWAP': handle_swap,
    'LIQUIDITY': handle_liquidity,
    'SEND_TO_FRIENDS': handle_send_to_friends_task,
}


class PharosClient:
    def __init__(self, private_key, proxy=None):
        self.wallet = Account.from_key(private_key)
        self.session = aiohttp.ClientSession(proxy=proxy if proxy else None)
        self.headers = pharos_headers


    async def login(self):
        url = f'https://api.pharosnetwork.xyz/user/login?address={self.wallet.address}&signature={sign_message(self.wallet, 'pharos')}'
        random_sleep = random.randint(20, 90)
        logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before login...')
        await asyncio.sleep(random_sleep)
        for _ in range(ATTEMPTS):
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
                        logger.error(self.wallet.address, f'Error while logging in: {await response.text()}. Retrying in {random_sleep} sec...')
                        await asyncio.sleep(random_sleep)
            except Exception as e:
                logger.error(self.wallet.address, f'An error occurred while logging in: {e}')


    async def get_user_data(self):
        url = f'https://api.pharosnetwork.xyz/user/profile?address={self.wallet.address}'

        for _ in range(ATTEMPTS):
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
        
        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
        logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before fetching faucets...')
        await asyncio.sleep(random_sleep)

        for _ in range(ATTEMPTS):
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
            for _ in range(ATTEMPTS):
                try:
                    await fetch_stable_faucet(self.session, self.wallet.address, stable)
                    break
                except Exception as e:
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    logger.error(self.wallet.address, f'An error occurred while fetching stable faucet: {e}. Retrying in {random_sleep} sec...')
                    await asyncio.sleep(random_sleep)


    async def check_in(self):
        for _ in range(ATTEMPTS):
            random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
            logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before daily checkin...')
            await asyncio.sleep(random_sleep)
            if await checkin(self.session, self.wallet.address, self.headers):
                break


    async def run_onchain(self):
        all_tasks = []
        task_amount = 0
        task_counter = 0
        
        for task_name, task_data in tasks.items():
            task_count = random.randint(task_data['TASK_COUNT'][0], task_data['TASK_COUNT'][1])
            all_tasks.append({task_name: task_count})
            task_amount += task_count
        
        random.shuffle(all_tasks)

        for task in all_tasks:
            for task_name, task_count in task.items():
                for _ in range(task_count):
                    for retry in range(ATTEMPTS):
                        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])

                        if task_name == 'SEND_TO_FRIENDS':
                            task_res = await tasks_functions[task_name](self.session, self.wallet, self.headers)
                            if task_res: 
                                task_counter += 1
                                break
                            elif not task_res and retry == ATTEMPTS - 1: task_counter += 1
                        else:
                            task_res = await tasks_functions[task_name](self.wallet)
                            if task_res:
                                task_counter += 1
                                break
                            elif not task_res and retry == ATTEMPTS - 1: task_counter += 1
                        logger.error(self.wallet.address, f'[{task_counter}/{task_amount}] | Error while completing {task_name} task, sleeping for {random_sleep} sec before next retry...')
                        await asyncio.sleep(random_sleep)
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    logger.info(self.wallet.address,  f'[{task_counter}/{task_amount}] | Sleeping for {random_sleep} sec before next task...')
                    await asyncio.sleep(random_sleep)


    async def connect_socials(self):
        pass
                

    async def close_session(self):
        if self.session:
            await self.session.close()