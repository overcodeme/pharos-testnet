from utils.logger import logger
from data.const import zenith_headers
import aiohttp



async def is_able_to_faucet(session: aiohttp.ClientSession, wallet_address, headers):
    url = f'https://api.pharosnetwork.xyz/faucet/status?address={wallet_address}'

    async with session.get(url=url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            if data['data']['is_able_to_faucet'] == True:
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
                logger.success(wallet_address, f'Successfully claimed native faucet')
            else:
                logger.warning(wallet_address, 'You already used native faucet today')

    else:
        logger.warning(wallet_address, 'Twitter not connected')


async def fetch_stable_faucet(session: aiohttp.ClientSession, wallet_address, token):
    url = 'https://testnet-router.zenithswap.xyz/api/v1/faucet'
    try:
        data = {
            'tokenAddress': token['contract_address'],
            'userAddress': wallet_address
        }
        async with session.post(url=url, headers=zenith_headers, json=data) as response:
            data = await response.json()
            if data['message'] == 'system error': raise Exception('Error while fetching stable faucet, retrying...')
            if response.status == 200: logger.success(wallet_address, f'Successfully claimed {token['name']} faucet')
    except Exception as e:
        logger.error(wallet_address, f'An error occurred while fetching stable faucet: {e}')
            
