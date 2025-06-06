from web3 import AsyncWeb3
from eth_account import Account
from anticaptchaofficial.recaptchav2proxyless import *
from colorama import Fore, Style
from data.abi import abi
from data.const import rpc
from utils.logger import logger
import aiohttp

w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))

async def is_able_to_faucet(session: aiohttp.ClientSession, wallet_address, headers):
    url = f'https://api.pharosnetwork.xyz/faucet/status?address={wallet_address}'

    async with session.get(url=url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            if data['is_able_to_faucet'] == True:
                return True
            else:
                return False
        else:
            logger.error(wallet_address, f'Error while checking faucet eligibelity: {await response.text()}')



async def fetch_native_faucet(session: aiohttp.ClientSession, wallet_address, is_twitter_connected, headers):
    if is_twitter_connected:
        url = f'https://api.pharosnetwork.xyz/faucet/daily?address={wallet_address}'

        async with session.post(url=url, headers=headers) as response:
            if response.status == 200:
                logger.success(wallet_address, 'Successfully claimed native faucet')
            else:
                logger.error(wallet_address, f'Error while claiming native faucet: {await response.text()}')

    else:
        logger.warning(wallet_address, 'Twitter not connected')


async def fetch_stable_faucet(wallet: Account, token_address):
    faucet_abi = abi['zenithFaucet']
    faucet_address = '0x11DE0e754f1Df7C7B0d559721b334809A9C0dfb7'
    contract = w3.eth.contract(address=faucet_address, abi=faucet_abi)

    tx = contract.functions.mint()


