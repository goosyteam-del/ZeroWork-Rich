"""
Configuration module for blockchain networks, tokens, and RPC endpoints
Contains all supported chains and token configurations
"""

from typing import Dict, List
import os


# Supported Networks Configuration
NETWORKS = {
    "ethereum": {
        "name": "Ethereum",
        "chain_id": 1,
        "rpc_url": os.getenv("ETHEREUM_RPC", "https://eth.llamarpc.com"),
        "native_token": "ETH",
        "explorer": "https://etherscan.io"
    },
    "bsc": {
        "name": "Binance Smart Chain",
        "chain_id": 56,
        "rpc_url": os.getenv("BSC_RPC", "https://bsc-dataseed1.binance.org"),
        "native_token": "BNB",
        "explorer": "https://bscscan.com"
    },
    "polygon": {
        "name": "Polygon",
        "chain_id": 137,
        "rpc_url": os.getenv("POLYGON_RPC", "https://polygon-rpc.com"),
        "native_token": "MATIC",
        "explorer": "https://polygonscan.com"
    },
    "arbitrum": {
        "name": "Arbitrum One",
        "chain_id": 42161,
        "rpc_url": os.getenv("ARBITRUM_RPC", "https://arb1.arbitrum.io/rpc"),
        "native_token": "ETH",
        "explorer": "https://arbiscan.io"
    },
    "optimism": {
        "name": "Optimism",
        "chain_id": 10,
        "rpc_url": os.getenv("OPTIMISM_RPC", "https://mainnet.optimism.io"),
        "native_token": "ETH",
        "explorer": "https://optimistic.etherscan.io"
    }
}


# Popular ERC-20 Tokens (address varies by network)
TOKENS = {
    "ethereum": [
        {"symbol": "USDT", "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "decimals": 6},
        {"symbol": "USDC", "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "decimals": 6},
        {"symbol": "DAI", "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "decimals": 18},
        {"symbol": "WETH", "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "decimals": 18},
        {"symbol": "WBTC", "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "decimals": 8},
    ],
    "bsc": [
        {"symbol": "USDT", "address": "0x55d398326f99059fF775485246999027B3197955", "decimals": 18},
        {"symbol": "USDC", "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d", "decimals": 18},
        {"symbol": "BUSD", "address": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56", "decimals": 18},
        {"symbol": "WBNB", "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c", "decimals": 18},
        {"symbol": "CAKE", "address": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82", "decimals": 18},
    ],
    "polygon": [
        {"symbol": "USDT", "address": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F", "decimals": 6},
        {"symbol": "USDC", "address": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", "decimals": 6},
        {"symbol": "DAI", "address": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063", "decimals": 18},
        {"symbol": "WMATIC", "address": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270", "decimals": 18},
        {"symbol": "WETH", "address": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619", "decimals": 18},
    ],
    "arbitrum": [
        {"symbol": "USDT", "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9", "decimals": 6},
        {"symbol": "USDC", "address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8", "decimals": 6},
        {"symbol": "DAI", "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", "decimals": 18},
        {"symbol": "WETH", "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "decimals": 18},
    ],
    "optimism": [
        {"symbol": "USDT", "address": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58", "decimals": 6},
        {"symbol": "USDC", "address": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607", "decimals": 6},
        {"symbol": "DAI", "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", "decimals": 18},
        {"symbol": "WETH", "address": "0x4200000000000000000000000000000000000006", "decimals": 18},
    ]
}


# ERC-20 ABI (minimal for balance checking)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]


# Price API Configuration
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Token ID mapping for price fetching
TOKEN_PRICE_IDS = {
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "MATIC": "matic-network",
    "BTC": "bitcoin",
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI": "dai",
    "WETH": "ethereum",
    "WBTC": "wrapped-bitcoin",
    "BUSD": "binance-usd",
    "CAKE": "pancakeswap-token",
    "WBNB": "binancecoin",
    "WMATIC": "matic-network"
}


# Trading Configuration
MIN_BALANCE_USD = float(os.getenv("MIN_BALANCE_USD", "5.0"))
ENABLE_MOCK_TRADING = os.getenv("ENABLE_MOCK_TRADING", "true").lower() == "true"
MOCK_TRADE_INTERVAL = int(os.getenv("MOCK_TRADE_INTERVAL", "10"))


# Mock Exchange Data (for arbitrage simulation)
MOCK_EXCHANGES = {
    "uniswap": {"name": "Uniswap", "fee": 0.003},
    "pancakeswap": {"name": "PancakeSwap", "fee": 0.0025},
    "sushiswap": {"name": "SushiSwap", "fee": 0.003},
    "quickswap": {"name": "QuickSwap", "fee": 0.003},
}


def get_network_config(network_name: str) -> Dict:
    """Get configuration for a specific network"""
    return NETWORKS.get(network_name.lower(), {})


def get_all_networks() -> List[str]:
    """Get list of all supported network names"""
    return list(NETWORKS.keys())


def get_tokens_for_network(network_name: str) -> List[Dict]:
    """Get token list for a specific network"""
    return TOKENS.get(network_name.lower(), [])
