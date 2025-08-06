from data.const import stables_data, faros_headers, rpc
from utils.abi import uniswap_v2
from web3 import AsyncWeb3
from eth_account.account import Account
from utils.utils import get_token_balance, get_tokens_with_balance, approve_token
from utils.file_manager import load_yaml
from utils.logger import logger
from colorama import Fore, Style
import time
import random
import aiohttp
import asyncio



settings = load_yaml('settings.yaml')
swap_router_address = '0x3541423f25A1Ca5C98fdBCf478405d3f0aaD1164'
dvm_router_address = '0x4b177AdEd3b8bD1D5D747F91B9E853513838Cd49'
pool_router_address = '0x73cafc894dbfc181398264934f7be4e482fc9d40'

pool_pair_addresses = [
    "0x3eb5a16afd6235fdeeda7966209ab6f78c0f302e", # USDC/USDT
    "0xed84211cbdcf93e4464f58dc7f10bdf6730fe0b5"  # USDT/USDC
]

tokens_data = [
    *stables_data,
    {'name': 'WETH', 'contract_address': '0x4E28826d32F1C398DED160DC16Ac6873357d048f', 'decimals': 18},
    {'name': 'WPHRS', 'contract_address': '0x76aaada469d23216be5f7c596fa25f282ff9b364', 'decimals': 18}
]

async def perform_dodo_request(wallet_address, from_token, to_token, amount, session: aiohttp.ClientSession, attempts=3):
    for _ in range(attempts):
        deadline = int(time.time()) + 300
        url = (
            f"https://api.dodoex.io/route-service/v2/widget/getdodoroute?chainId=688688&deadLine={deadline}"
            f"&apikey=a37546505892e1a952&slippage=3.225&source=dodoV2AndMixWasm&toTokenAddress={to_token}"
            f"&fromTokenAddress={from_token}&userAddr={wallet_address}&estimateGas=true&fromAmount={amount}"
        )

        try:
            async with session.get(url=url, headers=faros_headers) as response:
                data = await response.json()
                if response.status == 200:
                    return data
                else:
                    logger.error(wallet_address, f'Quote not available')
        except Exception as e:
            logger.error(wallet_address, f'An error occurred while fetching dodo request: {e}')
            await asyncio.sleep(random.randint(5, 15))
    return None


async def perform_faros_swap(session: aiohttp.ClientSession, wallet: Account, w3=AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))):
    try:
        swap_pairs = {'USDC': ['USDT', 'WETH'], 'USDC': ['USDT', 'WETH'], 'WETH': ['USDC', 'USDT']}
        tokens_with_balance = await get_tokens_with_balance(wallet.address)
        random.shuffle(tokens_with_balance)

        from_token = tokens_with_balance[0]
        to_token = tokens_data[random.choice(swap_pairs[from_token['name']])]

        token_balance = await get_token_balance(wallet.address, from_token)
        amount_in_wei = int(random.randint(settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][0], settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][1]) / 100 * token_balance)
        amount = round(amount_in_wei, 3)

        logger.info(wallet.address, f'{Fore.YELLOW}[FaroSwap]{Style.RESET_ALL} Trying to swap {amount} {tokens_data[from_token['name']]} to {tokens_data[to_token['name']]}')

        await approve_token(wallet, amount_in_wei)

        dodo_response = await perform_dodo_request(wallet.address, from_token, to_token, amount_in_wei, session)
        if not dodo_response:
            return False
        
        value = dodo_response.get('data', {}).get('value')
        calldata = dodo_response.get('data', {}).get('data')
        gas_limit = dodo_response.get('data', {}).get('gasLimit', 300000)

        max_priority_fee = int(w3.to_wei(1, 'gwei'))
        max_fee = max_priority_fee

        tx = {
            'chainId': 688688,
            'data': calldata,
            'from': wallet.address,
            'gas': gas_limit,
            'to': swap_router_address,
            'value': int(value),
            'maxPriorityFeePerGas': max_priority_fee,
            'maxFeePerGas': max_fee,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        }

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash.hex())

        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully swapped {tokens_data[from_token['name']]} to {tokens_data[to_token['name']]}')
        else:
            logger.error(wallet.address, f'Swap error: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while swap performing: {e}')


async def perform_faros_liquidity(wallet: Account, w3: AsyncWeb3):
    deadline = int(time.time()) + 300
    liq_pair = random.choice([['USDC', 'USDT'], ['USDT', 'USDC']])
    token1, token2 = tokens_data[liq_pair[0]], tokens_data[liq_pair[1]]
    balance = min(await get_token_balance(wallet.address, token1), await get_token_balance(wallet.address, token2))

    amount = int(random.randint(settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][0], settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][1]) / 100 * balance)
    min_amount = int(amount * 0.9)
    await approve_token(wallet, amount, token1, pool_router_address)
    await approve_token(wallet, amount, token2, pool_router_address)

    logger.info(wallet.address, f'[FaroSwap] Trying to add liquidity in {token1['name']}/{token2['name']} pair')

    contract = w3.eth.contract(address=w3.to_checksum_address(dvm_router_address), abi=uniswap_v2)
    pool_address = pool_pair_addresses[0] if token1['name'] == 'USDC' else pool_pair_addresses[1]
    dvm_address = w3.to_checksum_address(pool_address)

    add_lp_data = contract.functions.addDVMLiquidity(
        dvm_address, amount, amount, min_amount, min_amount, 0, deadline
    )

    max_priority_fee = int(w3.to_wei(1, 'gwei'))
    max_fee = max_priority_fee
    estimated_gas = add_lp_data.estimate_gas({'from': wallet.address, 'value': 0})

    tx = {
        'chainId': 688688,
        'from': wallet.address,
        'gas': int(estimated_gas * 1.2),
        "maxFeePerGas": int(max_fee),
        "maxPriorityFeePerGas": int(max_priority_fee),
        'nonce': await w3.eth.get_transaction_count(wallet.address),
        'value': 0
    }

    signed_tx = wallet.sign_transaction(tx)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash.hex())

    if tx_receipt.status == 1:
        logger.success(wallet.address, f'Successfully added liquidity in {token1['name']}/{token2['name']} pair')
    else:
        logger.error(wallet.address, f'')