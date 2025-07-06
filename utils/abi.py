erc20token_abi = [{"constant":True,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]

zenith_swap = [{
        "inputs": [
        {
            "components": [
              {
                "internalType": "address",
                "name": "tokenIn",
                "type": "address"
              },
              {
                "internalType": "address",
                "name": "tokenOut",
                "type": "address"
              },
              {
                "internalType": "uint24",
                "name": "fee",
                "type": "uint24"
              },
              {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "amountOutMinimum",
                "type": "uint256"
              },
              {
                "internalType": "uint160",
                "name": "sqrtPriceLimitX96",
                "type": "uint160"
              }
            ],
            "internalType": "struct IVRouter.ExactInputSingleParams",
            "name": "params",
            "type": "tuple"
        }
        ],
        "name": "exactInputSingle",
        "outputs": [
          {
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"
          }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
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
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        },
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
          "name": "",
          "type": "bytes[]"
        }
      ],
      "stateMutability": "payable",
      "type": "function"
    }
]

zenith_liquidity = [
  {
    "name": "mint",
    "type": "function",
    "inputs": [
      {
        "components": [
          {
            "name": "token0",
            "type": "address"
          },
          {
            "name": "token1",
            "type": "address"
          },
          {
            "name": "fee",
            "type": "uint24"
          },
          {
            "name": "tickLower",
            "type": "int24"
          },
          {
            "name": "tickUpper",
            "type": "int24"
          },
          {
            "name": "amount0Desired",
            "type": "uint256"
          },
          {
            "name": "amount1Desired",
            "type": "uint256"
          },
          {
            "name": "amount0Min",
            "type": "uint256"
          },
          {
            "name": "amount1Min",
            "type": "uint256"
          },
          {
            "name": "recipient",
            "type": "address"
          },
          {
            "name": "deadline",
            "type": "uint256"
          }
        ],
        "name": "params",
        "type": "tuple"
      }
    ],
    "outputs": [
      {
        "name": "tokenId",
        "type": "uint256"
      },
      {
        "name": "liquidity",
        "type": "uint128"
      },
      {
        "name": "amount0",
        "type": "uint256"
      },
      {
        "name": "amount1",
        "type": "uint256"
      }
    ],
    "stateMutability": "payable"
  },
  {
    "name": "increaseLiquidity",
    "type": "function",
    "inputs": [
      {
        "components": [
          {
            "name": "tokenId",
            "type": "uint256"
          },
          {
            "name": "amount0Desired",
            "type": "uint256"
          },
          {
            "name": "amount1Desired",
            "type": "uint256"
          },
          {
            "name": "amount0Min",
            "type": "uint256"
          },
          {
            "name": "amount1Min",
            "type": "uint256"
          },
          {
            "name": "deadline",
            "type": "uint256"
          }
        ],
        "name": "params",
        "type": "tuple"
      }
    ],
    "outputs": [
      {
        "name": "liquidity",
        "type": "uint128"
      },
      {
        "name": "amount0",
        "type": "uint256"
      },
      {
        "name": "amount1",
        "type": "uint256"
      }
    ],
    "stateMutability": "payable"
  },
  {
    "name": "multicall",
    "type": "function",
    "inputs": [
      {
        "name": "datas",
        "type": "bytes[]"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "bytes[]"
      }
    ],
    "stateMutability": "payable"
  },
  {
    "name": "balanceOf",
    "type": "function",
    "inputs": [
      {
        "name": "owner",
        "type": "address"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view"
  },
  {
    "name": "tokenOfOwnerByIndex",
    "type": "function",
    "inputs": [
      {
        "name": "owner",
        "type": "address"
      },
      {
        "name": "index",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view"
  },
  {
    "name": "positions",
    "type": "function",
    "inputs": [
      {
        "name": "tokenId",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "nonce",
        "type": "uint96"
      },
      {
        "name": "operator",
        "type": "address"
      },
      {
        "name": "token0",
        "type": "address"
      },
      {
        "name": "token1",
        "type": "address"
      },
      {
        "name": "fee",
        "type": "uint24"
      },
      {
        "name": "tickLower",
        "type": "int24"
      },
      {
        "name": "tickUpper",
        "type": "int24"
      },
      {
        "name": "liquidity",
        "type": "uint128"
      },
      {
        "name": "feeGrowthInside0LastX128",
        "type": "uint256"
      },
      {
        "name": "feeGrowthInside1LastX128",
        "type": "uint256"
      },
      {
        "name": "tokensOwed0",
        "type": "uint128"
      },
      {
        "name": "tokensOwed1",
        "type": "uint128"
      }
    ],
    "stateMutability": "view"
  }
]

faros_liquidity = [{
    "type": "function",
    "name": "addDVMLiquidity",
    "stateMutability": "payable",
    "inputs": [
        { "internalType": "address", "name": "dvmAddress", "type": "address" },
        { "internalType": "uint256", "name": "baseInAmount", "type": "uint256" },
        { "internalType": "uint256", "name": "quoteInAmount", "type": "uint256" },
        { "internalType": "uint256", "name": "baseMinAmount", "type": "uint256" },
        { "internalType": "uint256", "name": "quoteMinAmount", "type": "uint256" },
        { "internalType": "uint8", "name": "flag", "type": "uint8" },
        { "internalType": "uint256", "name": "deadLine", "type": "uint256" }
    ],
    "outputs": [
        { "internalType": "uint256", "name": "shares", "type": "uint256" },
        { "internalType": "uint256", "name": "baseAdjustedInAmount", "type": "uint256" },
        { "internalType": "uint256", "name": "quoteAdjustedInAmount", "type": "uint256" }
    ]
}]