faucet_address = '0x11DE0e754f1Df7C7B0d559721b334809A9C0dfb7'
router_address = '0x1a4de519154ae51200b0ad7c90f7fac75547888a'
liq_address = '0xF8a1D4FF0f9b9Af7CE58E1fc1833688F3BFd6115'
WPHRS_address = '0x76aaada469d23216be5f7c596fa25f282ff9b364'


rpc = 'https://testnet.dplabs-internal.com'

pharos_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'authorization': 'Bearer null',
    'content-length': '0',
    'origin': 'https://testnet.pharosnetwork.xyz',
    'priority': 'u=1, i',
    'referer': 'https://testnet.pharosnetwork.xyz/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

zenith_headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'origin': 'https://testnet.zenithswap.xyz',
    'priority': 'u=1, i',
    'referer': 'https://testnet.zenithswap.xyz/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}


stables_data = [
    {'name': 'USDC', 'contract_address': '0x72df0bcd7276f2dfbac900d1ce63c272c4bccced', 'decimals': 6},
    {'name': 'USDT', 'contract_address': '0xd4071393f8716661958f766df660033b3d35fd29', 'decimals': 6}
]

menu_items = [
    {'name': 'Faucet', 'description': 'Launch native and stables faucet', 'func': 'fetch_faucet'},
    {'name': 'Daily check-in', 'description': 'Complete daily check-in', 'func': 'check_in'},
    {'name': 'On-chain tasks', 'description': 'Swap, add liquidity, send to another wallet', 'func': 'run_onchain'},
    {'name': 'Mint badge', 'description': 'Mint pharos testnet badge', 'func': 'mint_testnet_badge'},
    {'name': 'Gotchipus NFT', 'description': 'Mint Gotchipus NFT', 'func': 'gotchipus_mint'},
    {'name': 'Connect socials', 'description': 'Connect discord and twitter', 'func': 'connect_social'},
    {'name': 'Exit', 'description': 'Leave the script'}
]