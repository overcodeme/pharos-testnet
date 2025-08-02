from eth_account import Account
from web3 import AsyncWeb3
from data.const import pharos_headers, stables_data, rpc
from utils.logger import logger
from utils.file_manager import load_yaml, load_txt, save_session, load_json
from utils.utils import sign_message, define_testnet_lvl, generate_random_username
from utils.decorators import handle_retries
from actions.pharos.checkin import checkin
from actions.pharos.faucet import fetch_native_faucet, fetch_stable_faucet, is_able_to_faucet
from actions.pharos.send_to_friends import handle_send_to_friends_task
from actions.zenith.zenith_swap import zenith_handle_swap
from actions.zenith.zenith_liquidity import zenith_add_liquidity
# from actions.zentrafi.zentrafi_buy_token import zentrafi_buy_random_token
from actions.mint_gotchipus_nft import gotchipus_mint
from actions.mint_badge import handle_badge_minting
from actions.primus_tip import send_tokens_via_primus
from colorama import Fore, Style
from datetime import datetime, timezone
import aiohttp
import asyncio
import random


discords = load_txt('data/discord_tokens.txt')
twitters = load_txt('data/twitter_tokens.txt')
settings = load_yaml('settings.yaml')
sessions = load_json('data/sessions.json')
ATTEMPTS, SLEEP_DURATION = settings['ATTEMPTS'], settings['SLEEP_DURATION']
tasks = settings['TASKS']
onchain_tasks_functions = {
    # 'BUY_TOKENS': zentrafi_buy_random_token,
    'SWAP': zenith_handle_swap,
    'LIQUIDITY': zenith_add_liquidity,
    'SEND_TO_FRIENDS': handle_send_to_friends_task,
    'SEND_TO_FRIENDS_VIA_PRIMUS': send_tokens_via_primus
}

class PharosClient:
    def __init__(self, private_key, proxy=None):
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
        self.wallet = Account.from_key(private_key)
        self.session = aiohttp.ClientSession(proxy=proxy if proxy else None)
        self.headers = pharos_headers


    async def handle_wallet(self):
        random_sleep = random.randint(20, 90)
        logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before starting...')
        await asyncio.sleep(random_sleep)
        token = sessions.get(self.wallet.address)

        if token:
            self.headers['authorization'] = f'Bearer {token}'
            user_data = await self.get_user_data()
            if user_data['code'] == 0:
                logger.info(self.wallet.address, f'Level: {Fore.YELLOW}{await define_testnet_lvl(user_data['data']['user_info']['TotalPoints'])}{Style.RESET_ALL} | Total points: {Fore.YELLOW}{user_data['data']['user_info']['TotalPoints']}{Style.RESET_ALL}')
        else:
            await self.login()

    @handle_retries(max_retries=ATTEMPTS)
    async def login(self):
        message = f'testnet.pharosnetwork.xyz wants you to sign in with your Ethereum account:\n{self.wallet.address}\n\nI accept the Pharos Terms of Service: testnet.pharosnetwork.xyz/privacy-policy/Pharos-PrivacyPolicy.pdf\n\nURI: https://testnet.pharosnetwork.xyz\nVersion: 1\n\nChain ID: 688688\n\nNonce: {await self.w3.eth.get_transaction_count(self.wallet.address)}\n\nIssued At: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z'
        url = f'https://api.pharosnetwork.xyz/user/login?address={self.wallet.address}&signature={sign_message(self.wallet, message)}&wallet=OKX+Wallet'

        try:
            async with self.session.post(url=url, headers=self.headers) as response:
                data = await response.json()
                if data['code'] == 0:
                    token = data['data']['jwt']
                    self.headers['authorization'] = f'Bearer {token}'
                    user_data = await self.get_user_data()
                    logger.info(self.wallet.address, f'Total points: {Fore.YELLOW}{user_data['data']['user_info']['TotalPoints']}{Style.RESET_ALL}')
                    save_session(session_data=[self.wallet.address, token])
                    return True
                else:
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    logger.error(self.wallet.address, f'Error while logging in: {await response.text()}. Retrying in {random_sleep} sec...')
                    await asyncio.sleep(random_sleep)
        except Exception as e:
            logger.error(self.wallet.address, f'An error occurred while logging in: {e}')

    @handle_retries(max_retries=ATTEMPTS)
    async def get_user_data(self):
        url = f'https://api.pharosnetwork.xyz/user/profile?address={self.wallet.address}'

        try:
            async with self.session.get(url=url, headers=self.headers) as response:
                data = await response.json()
                if data['msg'] == 'ok':
                    data = await response.json()
                    return data
                else:
                    data = await response.text()
                    if 'invalid token' in data:
                        await self.login()
                    else:
                        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                        logger.error(self.wallet.address, f'Error while getting user data: {await response.text()} Retrying in {random_sleep} sec...')
                        await asyncio.sleep(random_sleep)

        except Exception as e:
            logger.error(self.wallet.address, f'An error occurred while gettings user data: {e}')
            
    @handle_retries(max_retries=ATTEMPTS)
    async def fetch_faucet(self):
        results = {}
        user_data = await self.get_user_data()
        stables = stables_data
        is_twitter_connected = True if user_data['data']['user_info']['XId'] else False
        
        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
        logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before fetching faucets...')
        await asyncio.sleep(random_sleep)

        try:
            if await is_able_to_faucet(self.session, self.wallet.address, self.headers):
                if await fetch_native_faucet(self.session, self.wallet.address, is_twitter_connected, self.headers):
                    results['native_faucet'] = 'ok'
                else:
                    results['native_faucet'] = 'error'
            else:
                logger.warning(self.wallet.address, 'You already used native faucet today')
                results['native_faucet'] = 'ok'
        except Exception as e:
            random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
            logger.error(self.wallet.address, f'An error occurred while fetching native faucet: {e}. Retrying in {random_sleep} sec...')
            await asyncio.sleep(random_sleep)

        for stable in stables:
            for _ in range(ATTEMPTS):
                try:
                    if await fetch_stable_faucet(self.session, self.wallet.address, stable):
                        results['stable_faucet'] = 'ok'
                        break
                except Exception as e:
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    logger.error(self.wallet.address, f'An error occurred while fetching stable faucet: {e}. Retrying in {random_sleep} sec...')
                    await asyncio.sleep(random_sleep)

        if results['native_faucet'] == 'ok' and results['stable_faucet'] == 'ok':
            return True
        else:
            await self.fetch_faucet()


    @handle_retries(max_retries=ATTEMPTS)
    async def check_in(self):
        random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
        logger.info(self.wallet.address, f'Sleeping for {random_sleep} sec before daily checkin...')
        await asyncio.sleep(random_sleep)
        if await checkin(self.session, self.wallet.address, self.headers): return True


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
                            task_res = await handle_send_to_friends_task(self.session, self.wallet, self.headers, self.w3)
                            if task_res: 
                                task_counter += 1
                                break
                            elif not task_res and retry == ATTEMPTS - 1: task_counter += 1
                        else:
                            task_res = await onchain_tasks_functions[task_name](self.wallet, self.w3)
                            if task_res:
                                task_counter += 1
                                break
                            elif not task_res and retry == ATTEMPTS - 1: task_counter += 1
                        logger.error(self.wallet.address, f'[{task_counter}/{task_amount}] | Error while completing {task_name} task, sleeping for {random_sleep} sec before next retry...')
                        await asyncio.sleep(random_sleep)
                    random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
                    logger.info(self.wallet.address,  f'[{task_counter}/{task_amount}] | Sleeping for {random_sleep} sec before next task...')
                    await asyncio.sleep(random_sleep)


    @handle_retries(max_retries=ATTEMPTS)
    async def mint_gotchipus_nft(self):
        if await gotchipus_mint(self.wallet):
            return True


    async def mint_badge(self, badge_address):
        res = await handle_badge_minting(self.wallet, badge_address)
        if res: return True
        else:
            random_sleep = random.randint(SLEEP_DURATION[0], SLEEP_DURATION[1])
            logger.error(self.wallet.address, f'Error while minting badge. Retrying in {random_sleep} sec...')
            await asyncio.sleep(random_sleep)


    @handle_retries(max_retries=ATTEMPTS)
    async def send_tokens_via_social_media(self):
        platform = random.choice('x', 'tiktok', 'google')
        username = await generate_random_username(platform)
        if await send_tokens_via_primus(self.wallet, self.w3, platform, username):
            return True


    @handle_retries(max_retries=ATTEMPTS)
    async def connect_socials(self):
        pass
                

    async def close_session(self):
        if self.session:
            await self.session.close()