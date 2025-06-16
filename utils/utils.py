from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from data.const import rpc, abi, router_address, WPHRS_address, stables_data
from utils.logger import logger
import aiohttp
import random
import time


async def verify_task(session: aiohttp.ClientSession, wallet_address, headers, task_id, tx_hash):
    url = f'https://api.pharosnetwork.xyz/task/verify?address={wallet_address}&task_id={task_id}&tx_hash={tx_hash}'
    try:
        async with session.post(url=url, headers=headers) as response:
            data = await response.json()
            if not data['verified']:
                logger.error(wallet_address, f'Error while verifying task: {await response.text()}')
    except Exception as e:
        logger.error(wallet_address, f'An error occurred while verifying task: {e}')