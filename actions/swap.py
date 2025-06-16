from web3 import AsyncWeb3
from utils.file_manager import load_yaml
from utils.utils import approve_token, get_token_balance, get_tokens_with_balance
from data.const import rpc, abi, router_address, WPHRS_address, stables_data
from utils.logger import logger
import random
import time


settings = load_yaml('settings.yaml')

async def swap_from_native(wallet, token):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=router_address, abi=abi['zenith_abi'])
    try:
        balance = await w3.eth.get_balance(wallet.address)
        amount = random.randint(settings['TASKS']['SWAP']['SWAP_FROM_NATIVE'][0], settings['TASKS']['SWAP']['SWAP_FROM_NATIVE'][1]) / 100 * balance
        data = contract.encodeABI(fn_name='exactInputSingle', args=[WPHRS_address, token['contract_address'], 500, wallet.address, w3.to_wei(amount, 'ether'), 0, 0])
    
        estimate_gas = await contract.functions.multicall(int(time.time()) + 6000, [data]).estimate_gas({'value': w3.to_wei(amount, 'ether')})
        tx = await contract.functions.multicall(int(time.time()) + 6000, [data]).build_transaction({
            'value': w3.to_wei(amount, 'ether'),
            'gasLimit': estimate_gas * 2,
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
        amount = random.randint(settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][0], settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][1]) / 100 * balance
        data = contract.encodeABI(fn_name='exactInputSingle', args=[token1['contract_address'], token2['contract_address'], 500, wallet.address, w3.to_wei(amount, 'ether'), 0, 0]) 
        estimate_gas = await contract.functions.multicall(int(time.time()) + 6000, [data]).estimate_gas({'value': w3.to_wei(amount, 'ether')})   

        tx = await contract.functions.multicall(int(time.time()) + 6000, [data]).build_transaction({
            'value': w3.to_wei(amount, 'ether'),
            'gas': estimate_gas * 2,
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


async def handle_swap(wallet):
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
        logger.error(wallet.address, f'Error while handling random swap: {e}')