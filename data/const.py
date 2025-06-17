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

abi = {
    'erc20token': [{"constant":True,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}],
    'zenith_abi': [{ "inputs": [], "name": "getMaximumMintAmount", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "asset", "type": "address" }], "name": "isMintable", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "isPermissioned", "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "token", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }], "name": "mint", "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "uint256", "name": "newMaxMintAmount", "type": "uint256" }], "name": "setMaximumMintAmount", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address", "name": "asset", "type": "address" }, { "internalType": "bool", "name": "active", "type": "bool" }], "name": "setMintable", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "bool", "name": "value", "type": "bool" }], "name": "setPermissioned", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address[]", "name": "childContracts", "type": "address[]" }, { "internalType": "bool", "name": "state", "type": "bool" }], "name": "setProtectedOfChild", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [{ "internalType": "address[]", "name": "childContracts", "type": "address[]" }, { "internalType": "address", "name": "newOwner", "type": "address" }], "name": "transferOwnershipOfChild", "outputs": [], "stateMutability": "nonpayable", "type": "function" },{"inputs": [{"components": [{ "internalType": "address", "name": "tokenIn", "type": "address" },{ "internalType": "address", "name": "tokenOut", "type": "address" },{ "internalType": "uint24", "name": "fee", "type": "uint24" },{ "internalType": "address", "name": "recipient", "type": "address" },{ "internalType": "uint256", "name": "amountIn", "type": "uint256" },{ "internalType": "uint256", "name": "amountOutMinimum", "type": "uint256" },{ "internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160" }],"internalType": "struct IV3SwapRouter.ExactInputSingleParams","name": "params","type": "tuple"}],"name": "exactInputSingle","outputs": [{ "internalType": "uint256", "name": "amountOut", "type": "uint256" }],"stateMutability": "payable","type": "function"},{"inputs": [{ "internalType": "uint256", "name": "collectionAndSelfcalls", "type": "uint256" },{ "internalType": "bytes[]", "name": "data", "type": "bytes[]" }],"name": "multicall","outputs": [],"stateMutability": "nonpayable","type": "function"}, {"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"}],
    'liquidity': [{
      "inputs": [
        {
          "components": [
            {
              "internalType": "address",
              "name": "token0",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "token1",
              "type": "address"
            },
            {
              "internalType": "uint24",
              "name": "fee",
              "type": "uint24"
            },
            {
              "internalType": "int24",
              "name": "tickLower",
              "type": "int24"
            },
            {
              "internalType": "int24",
              "name": "tickUpper",
              "type": "int24"
            },
            {
              "internalType": "uint256",
              "name": "amount0Desired",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "amount1Desired",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "amount0Min",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "amount1Min",
              "type": "uint256"
            },
            {
              "internalType": "address",
              "name": "recipient",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "deadline",
              "type": "uint256"
            }
          ],
          "internalType": "struct INonfungiblePositionManager.MintParams",
          "name": "params",
          "type": "tuple"
        }
      ],
      "name": "mint",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        },
        {
          "internalType": "uint128",
          "name": "liquidity",
          "type": "uint128"
        },
        {
          "internalType": "uint256",
          "name": "amount0",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amount1",
          "type": "uint256"
        }
      ],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "refundETH",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes[]",
          "name": "data",
          "type": "bytes[]"
        }
      ],
      "name": "multicall",
      "outputs": [
        {
          "internalType": "bytes[]",
          "name": "results",
          "type": "bytes[]"
        }
      ],
      "stateMutability": "payable",
      "type": "function"
    }]
}

stables_data = [
    {'name': 'USDC', 'contract_address': '0x72df0bcd7276f2dfbac900d1ce63c272c4bccced', 'decimals': 6},
    {'name': 'USDT', 'contract_address': '0xd4071393f8716661958f766df660033b3d35fd29', 'decimals': 6}
]

menu_items = [
    {'name': 'Faucet', 'description': 'Launch native and stables faucet', 'func': 'fetch_faucet'},
    {'name': 'Daily check-in', 'description': 'Complete daily check-in', 'func': 'check_in'},
    {'name': 'On-chain tasks', 'description': 'Swap, add liquidity, send to another wallet', 'func': 'run_onchain'},
    {'name': 'Gotchipus NFT', 'description': 'Mint Gotchipus NFT', 'func': 'gotchipus_mint'},
    {'name': 'Connect socials', 'description': 'Connect discord and twitter', 'func': 'connect_social'},
    {'name': 'Exit', 'description': 'Leave the script'}
]