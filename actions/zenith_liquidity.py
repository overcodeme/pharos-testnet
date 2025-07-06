from web3 import AsyncWeb3
from eth_account import Account
from utils.file_manager import load_yaml
from utils.abi import zenith_liquidity
from data.const import rpc, stables_data, liq_address, WPHRS_address
from utils.utils import get_token_balance
from utils.logger import logger
import time
import random


settings = load_yaml('settings.yaml')

async def zenith_add_liquidity(wallet: Account, w3=AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))):
    try:
        contract = w3.eth.contract(address=w3.to_checksum_address(liq_address), abi=zenith_liquidity)
        token1 = random.choice(stables_data)
        token1_balance = await get_token_balance(wallet.address, token1)
        balance = int(await w3.eth.get_balance(wallet.address))
        amount_in_wei = int(random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * balance)
        amount1 = int(random.randint(settings['TASKS']['LIQUIDITY']['AMOUNT'][0], settings['TASKS']['LIQUIDITY']['AMOUNT'][1]) / 100 * token1_balance)
        logger.info(wallet.address, f'Trying add liquidity PHRS/{token1['name']}')
        deadline = int(time.time() + 1000)

        mint_data = contract.encode_abi(
            abi_element_identifier='mint',
            args=[(
                w3.to_checksum_address(WPHRS_address),
                w3.to_checksum_address(token1['contract_address']),
                500,
                217910,
                217930,
                amount_in_wei,
                amount1,
                0,
                0,
                wallet.address,
                deadline
            )]
        )

        refund_data = '0x12210e8a'

        # estimate_gas = await contract.functions.multicall([mint_data, refund_data]).estimate_gas({
        #     'chainId': 688688,
        #     'from': wallet.address,
        #     'gasPrice': await w3.eth.gas_price,
        #     'nonce': await w3.eth.get_transaction_count(wallet.address),
        #     'value': 0
        # })
        # print(estimate_gas)

        tx = await contract.functions.multicall([mint_data, refund_data]).build_transaction({
            'chainId': 688688,
            'from': wallet.address,
            'gas': random.randint(400000, 550000),
            'gasPrice': await w3.eth.gas_price,
            'nonce': await w3.eth.get_transaction_count(wallet.address),
            'value': amount_in_wei
        })

        signed_tx = wallet.sign_transaction(tx)
        tx_hash = await w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            logger.success(wallet.address, f'Successfully added PHRS/{token1['name']} liqudity')
            return True
        else:
            logger.error(wallet.address, f'Error while adding liquidity: {tx_receipt}')

    except Exception as e:
        logger.error(wallet.address, f'An error occurred while adding liquidity: {e}')