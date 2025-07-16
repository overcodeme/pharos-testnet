# from web3 import AsyncWeb3
# from eth_account import Account
# from utils.file_manager import load_yaml
# from utils.abi import zentrafi_abi
# from data.const import rpc, stables_data, liq_address, WPHRS_address, zentrafi_headers
# from utils.utils import get_token_balance
# from utils.logger import logger
# import time
# import random
# import aiohttp


# ca = '0x8d7834fdbb98f4d17e3C9a5De39CA62Ed491fDCe'


# async def zentrafi_buy_random_token(wallet: Account, session: aiohttp.ClientSession):
#     w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
#     bytes_proof = await _get_bytes_proof(session)
#     random_token_address = await _get_random_token(session)
#     contract = w3.eth.contract(address=w3.to_checksum_address(ca), abi=zentrafi_abi)
    
    


# async def _get_zentrafi_tokens(session: aiohttp.ClientSession):
#     url = 'https://api.goldsky.com/api/public/project_cm9y2l8nhz87901v63uba80gv/subgraphs/zentra-launchpad-pharos-testnet/254316d/gn'

#     data = {
#         "operationName": "GetPools",
#         "query": "query GetPools {\n  fairPools {\n    id\n    createdAt\n    __typename\n  }\n  bondingPools {\n    id\n    createdAt\n    __typename\n  }\n}",
#         "variables": {}
#     }

#     async with session.post(url=url, headers=zentrafi_headers, json=data) as response:
#         if response.status == 200:
#             data = await response.json()
#             return data
        

# async def _get_random_token(session: aiohttp.ClientSession):
#     tokens_data = await _get_zentrafi_tokens(session)
#     random_token_address = random.choice(tokens_data['data']['bondingPools'])
    
#     return random_token_address


# async def _get_bytes_proof(session: aiohttp.ClientSession):
#     url = 'https://api.zentrafi.xyz/api/bytes-proof'

#     async with session.get(url=url, headers=zentrafi_headers) as response:
#         if response.status == 200:
#             return await response.json()
