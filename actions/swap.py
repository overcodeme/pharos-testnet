from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from utils.utils import approve_token, get_token_balance, get_tokens_with_balance
from data.const import rpc, abi, router_address, WPHRS_address, stables_data
from utils.logger import logger
import random
import time


settings = load_yaml('settings.yaml')

async def swap_from_native(wallet: Account, token):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    token['contract_address'] = w3.to_checksum_address(token['contract_address'])
    contract = w3.eth.contract(address=w3.to_checksum_address(router_address), abi=abi['zenith_abi'])
    try:
        balance = float(w3.from_wei(await w3.eth.get_balance(wallet.address), 'ether'))
        amount = random.randint(settings['TASKS']['SWAP']['SWAP_FROM_NATIVE'][0], settings['TASKS']['SWAP']['SWAP_FROM_NATIVE'][1]) / 100 * balance
        data = contract.functions.exactInputSingle((WPHRS_address, token['contract_address'], 500, wallet.address, w3.to_wei(amount, 'ether'), 0, 0)).build_transaction({
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })['data']

        logger.info(wallet.address, f'Trying to swap {amount} PHRS to {token['name']}')

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
    token1['contract_address'] = w3.to_checksum_address(token1['contract_address'])
    token2['contract_address'] = w3.to_checksum_address(token2['contract_address'])
    contract = w3.eth.contract(address=token1['contract_address'], abi=abi['zenith_abi'])
    try:
        balance = float(w3.from_wei(await w3.eth.get_balance(wallet.address), 'ether'))
        amount = random.randint(settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][0], settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][1]) / 100 * balance
        await approve_token(wallet, amount, token1)
        data = contract.functions.exactInputSingle(token1['contract_address'], token2['contract_address'], 500, wallet.address, w3.to_wei(amount, 'ether'), 0, 0).build_transaction({
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })['data']
        estimate_gas = await contract.functions.multicall(int(time.time()) + 6000, [data]).estimate_gas({'value': w3.to_wei(amount, 'ether')})   

        logger.info(wallet.address, f'Trying to swap {amount}{token1['name']} to {token2['name']}')

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
                token1 = random.choice(tokens_with_balance)
                tokens_data.remove(token1)
                token2 = random.choice(tokens_data)
                await swap_from_stable(wallet, token1, token2)
    except Exception as e:
        logger.error(wallet.address, f'Error while handling random swap: {e}')