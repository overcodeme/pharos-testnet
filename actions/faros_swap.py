from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from utils.utils import approve_token, get_token_balance, get_tokens_with_balance
from utils.abi import zenith_swap
from data.const import rpc, router_address, WPHRS_address, stables_data
from utils.logger import logger
import random
import time


async def faroswap(wallet: Account, token1, token2):
    pass