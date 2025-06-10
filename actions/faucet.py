from web3 import AsyncWeb3
from eth_account import Account
from data.const import abi
from data.const import rpc, faucet_address
from utils.logger import logger
import aiohttp


w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))

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


async def fetch_stable_faucet(wallet: Account, token: dict):
    contract = w3.eth.contract(address=faucet_address, abi=abi['zenith_abi'])

    gas_limit = await contract.functions.mint(token['contract_address'], wallet.address, 1000000000000000000000).estimate_gas()
    tx = await contract.functions.mint(token['contract_address'], wallet.address, 1000000000000000000000).build_transaction({
        'chainId': 688688,
        'gasLimit': gas_limit * 1.5,
        'gasPrice': await w3.eth.gas_price,
        'nonce': await w3.eth.get_transaction_count(wallet.address),
    })

    signed_tx = wallet.sign_transaction(tx)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt.status == 1:
        logger.success(wallet.address, f'Successfully minted {token['name']}')
    else:
        logger.error(wallet.address, f'Error while minting {token['name']}: {tx_receipt}')

