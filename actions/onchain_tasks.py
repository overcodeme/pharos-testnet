from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from data.const import rpc, abi, router_address, WPHRS_address, stables_data
from utils.logger import logger
import aiohttp
import random
import time


settings = load_yaml('settings.yaml')

async def approve_token(wallet, amount, spender, token: dict):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=token['contract_address'], abi=abi['erc20token'])
    allowance_amount = (contract.functions.allowance(wallet.address, spender).call()) / (10 ** token['decimals'])

    if allowance_amount < amount:
        tx = contract.functions.approve(wallet.address, amount).build_transaction({
            'chainId': 688688,
            'gas': 150000,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully approved {token['name']}')
        else:
            logger.error(wallet.address, f'Token {token['name']} approve error: {tx_receipt}')


async def handle_liquidity(wallet):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    tokens_with_balance = await get_tokens_with_balance(wallet.address)
    token0 = {'name': 'PHRS', 'decimals': 18, 'balance': await w3.eth.get_balance(wallet.address)}
    token1 = tokens_with_balance[0]
    if len (tokens_with_balance) < 1: 
        await swap_from_native(wallet, random.choice(stables_data))
    else:
        try:
            amount0 = random.randint(settings.TASKS.LIQUIDITY.AMOUNT[0], settings.TASKS.LIQUIDITY.AMOUNT[1]) / 100 * token0['balance']
            amount1 = random.randint(settings.TASKS.LIQUIDITY.AMOUNT[0], settings.TASKS.LIQUIDITY.AMOUNT[1]) / 100 * token1['balance']
            logger.info(wallet.address, f'Trying add liquidity {token0["name"]}/{token1['name']}')


        except Exception as e:
            logger.error(wallet.address, f'An error occurred while adding liquidity: {e}')



