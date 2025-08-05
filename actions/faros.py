from data.const import stables_data, faros_headers, rpc
from utils.abi import faros_liquidity
from web3 import AsyncWeb3
from eth_account.account import Account
from utils.utils import get_token_balance, get_tokens_with_balance, approve_token
from utils.file_manager import load_yaml
from utils.logger import logger
import time
import random
import aiohttp
import asyncio



settings = load_yaml('settings.yaml')
swap_address = '0x3541423f25A1Ca5C98fdBCf478405d3f0aaD1164'
liq_address = '0x73cafc894dbfc181398264934f7be4e482fc9d40'
tokens_data = [
    *stables_data,
    {'name': 'WETH', 'contract_address': '0x4E28826d32F1C398DED160DC16Ac6873357d048f', 'decimals': 18},
    {'name': 'WBTC', 'contract_address': '0x8275c526d1bCEc59a31d673929d3cE8d108fF5c7', 'decimals': 18},
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


async def perform_faros_swap(wallet: Account, w3=AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))):
    try:
        tokens_with_balance = await get_tokens_with_balance(wallet.address)
        from_token_ind = 
        from_token = random.choice(0, len(tokens_with_balance))
        to_token = None
        token_balance = await get_token_balance(wallet.address, from_token)
        amount = int(random.randint(settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][0], settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][1]) / 100 * token_balance)

        await approve_token(wallet, amount)




async def faros_add_liquidity(wallet: Account, w3: AsyncWeb3):
    contract = w3.eth.contract(address=w3.to_checksum_address(liq_address), abi=faros_liquidity)
    tokens = stables_data
    random.shuffle(tokens)

    deadline = int(time.time() + 600)
    stable1_balance = await get_token_balance(wallet.address, tokens[0])
    stable2_balance = await get_token_balance(wallet.address, tokens[1])
    amount = int(random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * min(stable1_balance, stable2_balance))
    logger.info(wallet.address, f'Trying to add liquidity in pair {tokens[0]['name']}/{tokens[1]['name']}')

    add_lp_data = await contract.functions.addDVMLiquidity(
        w3.to_checksum_address(liq_address, amount, amount, 0, 0, deadline)
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