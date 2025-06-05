from web3 import AsyncWeb3
from eth_account import Account


w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(''))

async def gotchipus_mint(private_key):
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