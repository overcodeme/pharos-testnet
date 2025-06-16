from web3 import AsyncWeb3
from eth_account import Account
from data.const import rpc
import random
from utils.file_manager import load_yaml
from utils.logger import logger
from utils.utils import verify_task
import aiohttp


settings = load_yaml('settings.yaml')

async def handle_send_to_friends_task(session: aiohttp.ClientSession, wallet, headers):
    tx_hash = await transfer_phrs(wallet)
    await verify_task(session, wallet.address, headers, '103', tx_hash)


async def transfer_phrs(wallet):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    balance = w3.eth.get_balance(wallet.address)
    amount = random.randint(settings['TASKS']['SEND_TO_FRIENDS']['AMOUNT'][0], settings['TASKS']['SEND_TO_FRIENDS']['AMOUNT'][1]) / 100 * balance

    try:
        random_address = Account.create().address

        tx = {
            'chainId': 688688,
            'to': random_address,
            'gas': 150000,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'value': w3.to_wei(amount, 'ether')
        }

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully sent {amount} PHRS to {random_address}')
            return f'0x{tx_hash}'
        else:
            logger.error(wallet.address, f'Error while sending on another wallet: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred: {e}')