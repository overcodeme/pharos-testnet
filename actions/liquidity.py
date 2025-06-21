from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from utils.utils import get_tokens_with_balance, approve_token, get_token_balance
from utils.abi import zenith_abi
from actions.swap import swap_from_native
from data.const import rpc, stables_data, liq_address, WPHRS_address
from utils.logger import logger
import time
import random


settings = load_yaml('settings.yaml')

async def add_liquidity(wallet: Account, token0, token1):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    try:
        contract = w3.eth.contract(address=w3.to_checksum_address(liq_address), abi=zenith_abi)
        balance = await w3.eth.get_balance(wallet.address)
        amount_in_wei = int(random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * balance)
        logger.info(wallet.address, f'Trying add liquidity {token0["name"]}/{token1['name']}')
        await approve_token(wallet, amount_in_wei, token1)
        deadline = int(time.time() + 1200)
        mint_data = contract.encode_abi(abi_element_identifier="mint", args=[(w3.to_checksum_address(WPHRS_address), w3.to_checksum_address(token1['contract_address']), 3000, 79620, 89400, amount_in_wei, 0, amount_in_wei, 0, wallet.address, deadline)])
        refund_data = '0x12210e8a'

        estimate_gas = await contract.functions.multicall([mint_data, refund_data]).estimate_gas({
            'from': wallet.address,
            'value': 0
        })

        tx = await contract.functions.multicall([mint_data, refund_data]).build_transaction({
            'value': amount_in_wei,
            'gas': estimate_gas * 1.5,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 200:
            logger.success(wallet.address, f'Successfully added {token0['name']}/{token1['name']} liqudity')
        else:
            logger.error(wallet.address, f'Error while adding liquidity: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while adding liquidity: {e}')


async def handle_liquidity(wallet):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    tokens_with_balance = await get_tokens_with_balance(wallet.address)
    token0 = {'name': 'PHRS', 'decimals': 18, 'balance': await w3.eth.get_balance(wallet.address)}
    token1 = tokens_with_balance[0]

    if len(tokens_with_balance) < 1: 
        await swap_from_native(wallet, random.choice(stables_data))
    else:
        await add_liquidity(wallet, token0, token1)