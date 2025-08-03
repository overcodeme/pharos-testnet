import random
from eth_account import Account
from utils.abi import primus_abi
from utils.file_manager import load_yaml
from utils.logger import logger
from web3 import AsyncWeb3


settings = load_yaml('settings.yaml')
ca = '0xd17512b7ec12880bd94eca9d774089ff89805f02'

async def send_tokens_via_primus(wallet: Account, w3: AsyncWeb3, platform: str, username: str):
    balance = float(w3.from_wei(await w3.eth.get_balance(wallet.address), 'ether'))
    amount = (random.randint(settings['TASKS']['SEND_TO_FRIENDS_VIA_PRIMUS']['AMOUNT'][0], settings['TASKS']['SEND_TO_FRIENDS_VIA_PRIMUS']['AMOUNT'][1]) / 100) * balance
    contract = w3.eth.contract(address=w3.to_checksum_address(ca), abi=primus_abi)

    amount_in_wei = w3.to_wei(amount, 'ether')

    tip_token = {
        'tokenType': 1,
        'tokenAddress': '0x0000000000000000000000000000000000000000'
    }

    tip_recipient = {
        "idSource": platform,
        "id": username,
        "amount": amount_in_wei,
        "nftIds": []
    }
    
    tx = await contract.functions.tip(tip_token, tip_recipient).build_transaction({
        'chainId': 688688,
        'from': wallet.address,
        'nonce': await w3.eth.get_transaction_count(wallet.address),
        'gas': random.randint(275000, 325000),
        'gasPrice': await w3.eth.gas_price,
        'value': amount_in_wei,
    })

    signed_tx = wallet.sign_transaction(tx)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash.hex())
    if tx_receipt.status == 1:
        logger.success(wallet.address, f'Successfully sent {amount} PHRS to {username}')
        return True
    else:
        logger.error(wallet.address, f'Error while sending tokens via social media: {tx_receipt}')