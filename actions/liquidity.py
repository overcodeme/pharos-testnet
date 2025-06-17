from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from utils.utils import get_tokens_with_balance, approve_token
from actions.swap import swap_from_native
from data.const import rpc, stables_data, liq_address, abi, WPHRS_address
from utils.logger import logger
import time
import random


settings = load_yaml('settings.yaml')

async def add_liquidity(wallet: Account, token0, token1):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    try:
        contract = w3.eth.contract(address=liq_address, abi=abi['liquidity'])
        amount0 = random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * token0['balance']
        amount1 = random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * token1['balance']
        logger.info(wallet.address, f'Trying add liquidity {token0["name"]}/{token1['name']}')

        await approve_token(wallet, amount1, token1)

        mint_data = contract.functions.mint(WPHRS_address, token1['contract_address'], 500, 55530, 55550, w3.to_wei(amount0), w3.to_wei(amount1), 0, 0, wallet.address, int(time.time()) + 6000).encodeABI()
        refund_data = contract.encodeABI(fn_name='refundETH', args=[])
        multicall_data = [mint_data, refund_data]
        estimate_gas = await contract.functions.multicall(multicall_data).estimate_gas({'value': str(amount0)})

        tx = await contract.functions.multicall(multicall_data).build_transaction({
            'value': w3.to_wei(amount0),
            'gas': estimate_gas * 2,
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