from web3 import AsyncWeb3
from eth_account import Account
from eth_account.messages import encode_defunct
from data.const import rpc, stables_data
from utils.logger import logger
from utils.abi import erc20token_abi, erc721_abi
import aiohttp
import random
import json


def sign_message(wallet: Account, message):
    encoded_message = encode_defunct(text=message)
    signature = wallet.sign_message(encoded_message)
    return f'0x{signature.signature.hex()}'


async def verify_task(session: aiohttp.ClientSession, wallet_address, headers, task_id, tx_hash, ssl):
    url = 'https://api.pharosnetwork.xyz/task/verify'

    data = {
        'address': str(wallet_address),
        'task_id': task_id,
        'tx_hash': str(tx_hash)
    }

    json_data = json.dumps(data)

    headers['content-length'] = str(len(json_data))
    headers['content-type'] = 'application/json'

    try:
        async with session.post(url=url, headers=headers, json=data, ssl=ssl) as response:
            data = await response.json()
            if data['data']['verified'] != True:
                logger.error(wallet_address, f'Error while verifying task: {await response.text()}')
                return False
            return True
    except Exception as e:
        logger.error(wallet_address, f'An error occurred while verifying task: {e}')
        return False


async def get_token_balance(wallet_address, token: dict):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=w3.to_checksum_address(token['contract_address']), abi=erc20token_abi)
    balance = await contract.functions.balanceOf(wallet_address).call()
    return balance


async def get_tokens_with_balance(wallet_address) -> list:
    tokens = [*stables_data]
    random.shuffle(tokens)
    result = []

    for token in tokens:
        balance = await get_token_balance(wallet_address, token)
        if balance > 0:
            result.append(token)

    return result


async def approve_token(wallet: Account, amount, token: dict, spender):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(address=w3.to_checksum_address(token['contract_address']), abi=erc20token_abi)
    allowance_amount = (await contract.functions.allowance(wallet.address, spender).call()) / (10 ** token['decimals'])

    if allowance_amount < amount:
        estimate_gas = await contract.functions.approve(spender, 1000000000000).estimate_gas({
            'chainId': 688688,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })

        tx = await contract.functions.approve(spender, 1000000000000).build_transaction({
            'chainId': 688688,
            'gas': estimate_gas * 2,
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address)
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully approved {token['name']}')
        else:
            logger.error(wallet.address, f'Token {token['name']} approve error: {tx_receipt}')


async def define_testnet_lvl(points: int):
    if points >= 6001: return 4
    if points >= 3501: return 3
    if points >= 1001: return 2
    return 1


async def is_nft_minted(wallet: Account, nft_address):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    contract = w3.eth.contract(w3.to_checksum_address(nft_address), abi=erc721_abi)

    if await contract.functions.balanceOf(wallet.address).call() > 0:
        return True
    