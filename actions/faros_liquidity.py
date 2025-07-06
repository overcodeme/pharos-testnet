from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from utils.abi import faros_liquidity
from data.const import rpc, stables_data, liq_address, WPHRS_address
from utils.utils import get_token_balance
from utils.logger import logger
import time
import random

settings = load_yaml('settings.yaml')
pool_address = '0x73cafc894dbfc181398264934f7be4e482fc9d40'

async def faros_add_liquidity(wallet: Account, w3: AsyncWeb3):
    contract = w3.eth.contract(address=w3.to_checksum_address(pool_address), abi=faros_liquidity)
    tokens = stables_data
    random.shuffle(tokens)

    deadline = int(time.time() + 600)
    stable1_balance = await get_token_balance(wallet.address, tokens[0])
    stable2_balance = await get_token_balance(wallet.address, tokens[1])
    amount = int(random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * min(stable1_balance, stable2_balance))
    logger.info(wallet.address, f'Trying to add liquidity in pair {tokens[0]['name']}/{tokens[1]['name']}')

    add_lp_data = await contract.functions.addDVMLiquidity(
        w3.to_checksum_address(pool_address, amount, amount, 0, 0, deadline)
    )

    estimate_gas = await add_lp_data.estimate_gas({
        'from': wallet.address,
        'value': 0
    })

    max_priority_fee = w3.to_wei(1, 'gwei')
    max_fee = max_priority_fee

    tx = add_lp_data.build_transaction({
        'chainId': 688688,
        'from': wallet.address,
        'gas': int(estimate_gas * 1.5),
        'nonce': await w3.eth.get_transaction_count(wallet.address),
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee
    })

    signed_tx = wallet.sign_transaction(tx)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt == 1:
        logger.success(wallet.address, f'Successfully added liquidity')
        return True
    else:
        logger.error(wallet.address, f'Error while adding liquidity: {tx_receipt}')