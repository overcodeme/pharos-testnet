from web3 import AsyncWeb3
from eth_account import Account
from data.const import rpc
from utils.logger import logger


async def gotchipus_mint(private_key):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    wallet = Account.from_key(private_key)

    tx = {
        "chainId": 688688,
        "data": "0x5b70ea9f",
        "from": wallet.address,
        "gasPrice": w3.eth.gas_price,
        "nonce": await w3.eth.get_transaction_count(wallet.address),
        "to": "0x0000000038f050528452D6Da1E7AACFA7B3Ec0a8"
    }

    tx['gas'] = w3.eth.estimate_gas(tx)

    signed_tx = wallet.sign_transaction(tx)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt.status == 1:
        logger.success(wallet.address, 'Successfully mited gotchipus NFT')
    else:
        logger.error(wallet.address, f'Error while minting gotchipus NFT: {tx_receipt}')