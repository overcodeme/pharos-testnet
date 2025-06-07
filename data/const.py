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

abi = {
    'erc20token': [{"constant":True,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}],
    'zenithFaucet': [{ "inputs": [], "name": "getMaximumMintAmount", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "asset", "type": "address" }], "name": "isMintable", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "isPermissioned", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "token", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "mint", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "uint256", "name": "newMaxMintAmount", "type": "uint256" }], "name": "setMaximumMintAmount", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "asset", "type": "address" }, { "internalType": "bool", "name": "active", "type": "bool" }], "name": "setMintable", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "bool", "name": "value", "type": "bool" }], "name": "setPermissioned", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address[]", "name": "childContracts", "type": "address[]" }, { "internalType": "bool", "name": "state", "type": "bool" }], "name": "setProtectedOfChild", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address[]", "name": "childContracts", "type": "address[]" }, { "internalType": "address", "name": "newOwner", "type": "address" }], "name": "transferOwnershipOfChild", "outputs": [], "stateMutability": "nonpayable", "type": "function" }],
    'liquidity': []
}

stables_faucet_data = [
    {'name': 'USDC', 'contract_address': '0xAD902CF99C2dE2f1Ba5ec4D642Fd7E49cae9EE37'},
    {'name': 'USDT', 'contract_address': '0xEd59De2D7ad9C043442e381231eE3646FC3C2939'}
]

menu_items = [
    {'name': 'Faucet', 'description': 'Launch native and stables faucet', 'func': 'fetch_faucet'},
    {'name': 'Daily check-in', 'description': 'Complete daily check-in', 'func': 'check_in'},
    {'name': 'On-chain tasks', 'description': 'Swap, add liquidity, send to another wallet', 'func': 'run_onchain'},
    {'name': 'Gotchipus NFT', 'description': 'Mint Gotchipus NFT', 'func': 'mint_gotchipus'},
    {'name': 'Connect socials', 'description': 'Connect discord and twitter', 'func': 'connect_socials'},
    {'name': 'Exit', 'description': 'Leave the script'}
]