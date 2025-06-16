from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from data.const import rpc, abi, router_address, WPHRS_address, stables_data
from utils.logger import logger
import aiohttp
import random
import time


async def verify_task(session: aiohttp.ClientSession, wallet_address, headers, task_id, tx_hash):
    url = f'https://api.pharosnetwork.xyz/task/verify?address={wallet_address}&task_id={task_id}&tx_hash={tx_hash}'
    try:
        async with session.post(url=url, headers=headers) as response:
            data = await response.json()
            if not data['verified']:
                logger.error(wallet_address, f'Error while verifying task: {await response.text()}')
    except Exception as e:
        logger.error(wallet_address, f'An error occurred while verifying task: {e}')


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