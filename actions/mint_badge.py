from web3 import AsyncWeb3
from eth_account import Account
from data.const import rpc
from utils.logger import logger
import random


async def mint_badge(wallet: Account, w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))):
    try:
        tx = {
            'chainId': 688688,
            'data': f'0x84bb1e42{wallet.address[2:].zfill(64)}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            'from': wallet.address,
            'gas': random.randint(300000, 400000),
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'value': w3.to_wei(1, 'ether')
        }

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt.status == 1:
            logger.success(wallet.address, 'Successfully minted badge')
            return True
    except Exception as e:
        logger.error(wallet.address, f'An error occurred while badge minting: {e}')