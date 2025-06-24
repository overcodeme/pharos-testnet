from web3 import AsyncWeb3
from eth_account import Account
from eth_abi import encode
from utils.file_manager import load_yaml
from utils.utils import approve_token, get_token_balance, get_tokens_with_balance
from utils.abi import zenith_abi
from data.const import rpc, router_address, WPHRS_address, stables_data
from utils.logger import logger
import random
import time


settings = load_yaml('settings.yaml')

async def swap_from_native(wallet: Account, token):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=w3.to_checksum_address(router_address), abi=zenith_abi)
    try:
        balance = int(await w3.eth.get_balance(wallet.address))
        amount_in_wei = int(random.randint(settings['TASKS']['SWAP']['SWAP_FROM_NATIVE'][0], settings['TASKS']['SWAP']['SWAP_FROM_NATIVE'][1]) / 100 * balance)
        amount = w3.from_wei(amount_in_wei, 'ether')
        deadline = int(time.time() + 1200)

        logger.info(wallet.address, f'Trying to swap {amount} PHRS to {token['name']}')

        exact_input_data = contract.encode_abi(
            abi_element_identifier='exactInputSingle',
            args=[(
                w3.to_checksum_address(WPHRS_address),
                w3.to_checksum_address(token['contract_address']),
                500,
                wallet.address,
                amount_in_wei,
                0,
                0
            )]
        )

        estimate_gas = await contract.functions.multicall(deadline, [exact_input_data]).estimate_gas({
            'chainId': 688688,
            'from': wallet.address,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'gas': random.randint(245000, 300000),
            'gasPrice': int(await w3.eth.gas_price * 1.2),
            'value': amount_in_wei
        })

        tx = await contract.functions.multicall(deadline, [exact_input_data]).build_transaction({
            'chainId': 688688,
            'from': wallet.address,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'gas': estimate_gas * 2,
            'gasPrice': int(await w3.eth.gas_price * 1.2),
            'value': amount_in_wei
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully swapped {amount} PHRS to {token['name']}')
            return True
        else:
            logger.error(wallet.address, f'Swap error: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while swapping from native: {e}')


async def swap_from_stable(wallet: Account, token1, token2):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=w3.to_checksum_address(router_address), abi=zenith_abi)
    try:
        balance = await get_token_balance(wallet.address, token1)
        amount_in_wei = int(random.randint(settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][0], settings['TASKS']['SWAP']['SWAP_FROM_STABLE'][1]) / 100 * balance)
        amount = amount_in_wei / (10 ** token1['decimals'])
        await approve_token(wallet, amount, token1, w3.to_checksum_address(router_address))
        deadline = int(time.time() + 1200)

        logger.info(wallet.address, f'Trying to swap {amount} {token1['name']} to {token2['name']}')

        exact_input_data = contract.encode_abi(
            abi_element_identifier='exactInputSingle',
            args=[(
                w3.to_checksum_address(token1['contract_address']),
                w3.to_checksum_address(token2['contract_address']),
                500,
                wallet.address,
                amount_in_wei,
                0,
                0
            )]
        )

        estimate_gas = await contract.functions.multicall(deadline, [exact_input_data]).estimate_gas({
            'chainId': 688688,
            'from': wallet.address,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'gas': random.randint(245000, 300000),
            'gasPrice': int(await w3.eth.gas_price * 1.2)
        })

        tx = await contract.functions.multicall(deadline, [exact_input_data]).build_transaction({
            'chainId': 688688,
            'from': wallet.address,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'gas': estimate_gas * 2,
            'gasPrice': int(await w3.eth.gas_price * 1.2)
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully swapped {amount} {token1['name']} to {token2['name']}')
            return True
        else:
            logger.error(wallet.address, f'Swap error: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while swapping from stable: {e}')


async def handle_swap(wallet):
    tokens_data = [*stables_data]
    swap_from = 'native' if random.randint(1, 100) < 50 else 'stable'

    try:
        if swap_from == 'native':
            swap_to = random.choice(stables_data)
            if await swap_from_native(wallet, swap_to): return True
        else:
            tokens_with_balance = await get_tokens_with_balance(wallet.address)
            if len(tokens_with_balance) < 1:
                swap_to = random.choice(stables_data)
                if await swap_from_native(wallet, swap_to): return True
            else:
                token1 = random.choice(tokens_with_balance)
                tokens_data.remove(token1)
                token2 = random.choice(tokens_data)
                if await swap_from_stable(wallet, token1, token2): return True
    except Exception as e:
        logger.error(wallet.address, f'Error while handling random swap: {e}')