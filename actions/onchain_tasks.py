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


async def get_token_balance(wallet_address, token: dict):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=token['contract_address'], abi=abi['erc20token'])
    balance = await contract.functiions.balanceOf(wallet_address).call()
    return balance / (10 ** token['decimals'])


async def get_tokens_with_balance(wallet_address) -> list:
    tokens_data = [*stables_data]
    random.shuffle(tokens_data)
    result = []

    for token in tokens_data:
        balance = await get_token_balance(wallet_address, token)
        if balance > 0:
            result.append({'name': token['name'], 'balance': balance})

    return result


async def swap_from_native(wallet, token):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=router_address, abi=abi['zenith_abi'])
    try:
        balance = await w3.eth.get_balance(wallet.address)
        amount = random.randint(settings.TASKS.SWAP.SWAP_FROM_NATIVE[0], settings.TASKS.SWAP.SWAP_FROM_NATIVE[1]) / 100 * balance
        data = contract.encodeABI(fn_name='exactInputSingle', args=[WPHRS_address, token['contract_address'], 500, wallet.address, w3.to_wei(amount, 'ether'), 0, 0])
    
        gas_limit = await contract.functions.multicall(int(time.time()) + 6000, [data]).estimate_gas({'value': w3.to_wei(amount, 'ether')})
        tx = await contract.functions.multicall(int(time.time()) + 6000, [data]).build_transaction({
            'value': w3.to_wei(amount, 'ether'),
            'gasLimit': gas_limit * 1.5,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully swapped {amount} PHRS to {token['name']}')
        else:
            logger.error(wallet.address, f'Swap error: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while swapping from native: {e}')


async def swap_from_stable(wallet, token1, token2):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    await approve_token(wallet, amount, token1)
    contract = w3.eth.contract(address=token1['contract_address'], abi=abi['zenith_abi'])
    try:
        balance = await get_token_balance(wallet.address, token1)
        amount = random.randint(settings.TASKS.SWAP.SWAP_FROM_STABLE[0], settings.TASKS.SWAP.SWAP_FROM_STABLE[1]) / 100 * balance
        data = contract.encodeABI(fn_name='exactInputSingle', args=[token1['contract_address'], token2['contract_address'], 500, wallet.address, w3.to_wei(amount, 'ether'), 0, 0]) 
        gas_limit = await contract.functions.multicall(int(time.time()) + 6000, [data]).estimate_gas({'value': w3.to_wei(amount, 'ether')})   

        tx = await contract.functions.multicall(int(time.time()) + 6000, [data]).build_transaction({
            'value': w3.to_wei(amount, 'ether'),
            'gasLimit': gas_limit * 1.5,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.addres, f'Successfully swapped {amount}{token1['name']} to {token2['name']}')
        else:
            logger.error(wallet.address, f'Swap error: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while swapping from stable: {e}')


async def handle_random_swap(wallet):
    tokens_data = [*stables_data, {'name': 'WPHRS', 'contract_address': WPHRS_address, 'decimals': 18}]
    swap_from = 'native' if random.randint(1, 100) < 50 else 'stable'

    try:
        if swap_from == 'native':
            swap_to = random.choice(stables_data)
            await swap_from_native(wallet, swap_to)
        else:
            tokens_with_balance = await get_tokens_with_balance(wallet.address)
            if len(tokens_with_balance) < 1:
                swap_to = random.choice(stables_data)
                await swap_from_native(wallet, swap_to)
            else:
                token1 = tokens_data[random.choice(tokens_with_balance)['name']]
                tokens_data.pop(token1)
                token2 = random.choice(tokens_data)
                await swap_from_stable(wallet, token1, token2)
    except Exception as e:
        logger.error(wallet.address, f'Error while handling random swap function: {e}')


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



