"""
Balance Checker Module
Checks wallet balances across multiple networks and tokens
Converts all balances to USD for aggregation
"""

from web3 import Web3
from typing import Dict, List, Optional
import requests
import time
from src.config import (
    NETWORKS, TOKENS, ERC20_ABI, 
    COINGECKO_API, TOKEN_PRICE_IDS,
    get_all_networks, get_tokens_for_network
)
from src.logger_config import setup_logger

logger = setup_logger("BalanceChecker")


class BalanceChecker:
    """
    Checks balances across multiple blockchain networks
    """
    
    def __init__(self, wallet_address: str):
        """
        Initialize balance checker
        
        Args:
            wallet_address: Ethereum wallet address
        """
        self.wallet_address = Web3.to_checksum_address(wallet_address)
        self.price_cache: Dict[str, float] = {}
        self.price_cache_time: float = 0
        self.cache_duration: int = 300  # 5 minutes
        
    def _get_web3_connection(self, network_name: str) -> Optional[Web3]:
        """
        Create Web3 connection for a network
        
        Args:
            network_name: Name of the network
            
        Returns:
            Web3 instance or None on error
        """
        try:
            network_config = NETWORKS.get(network_name)
            if not network_config:
                logger.error(f"Unknown network: {network_name}")
                return None
            
            w3 = Web3(Web3.HTTPProvider(network_config["rpc_url"]))
            
            # Test connection
            if not w3.is_connected():
                logger.warning(f"Failed to connect to {network_config['name']}")
                return None
            
            return w3
            
        except Exception as e:
            logger.error(f"Error connecting to {network_name}: {str(e)}")
            return None
    
    def _fetch_token_prices(self) -> Dict[str, float]:
        """
        Fetch token prices from CoinGecko
        Uses cache to avoid rate limiting
        
        Returns:
            Dictionary of token symbol to USD price
        """
        current_time = time.time()
        
        # Return cached prices if still valid
        if self.price_cache and (current_time - self.price_cache_time) < self.cache_duration:
            return self.price_cache
        
        try:
            # Get all unique token IDs
            token_ids = ",".join(set(TOKEN_PRICE_IDS.values()))
            
            url = f"{COINGECKO_API}/simple/price"
            params = {
                "ids": token_ids,
                "vs_currencies": "usd"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            price_data = response.json()
            
            # Map back to token symbols
            prices = {}
            for symbol, coin_id in TOKEN_PRICE_IDS.items():
                if coin_id in price_data and "usd" in price_data[coin_id]:
                    prices[symbol] = price_data[coin_id]["usd"]
            
            self.price_cache = prices
            self.price_cache_time = current_time
            
            logger.info(f"✓ Fetched prices for {len(prices)} tokens")
            return prices
            
        except Exception as e:
            logger.warning(f"Failed to fetch prices from CoinGecko: {str(e)}")
            # Return cached prices even if expired, or empty dict
            return self.price_cache if self.price_cache else {}
    
    def _get_native_balance(self, w3: Web3, network_name: str) -> Dict[str, any]:
        """
        Get native token balance (ETH, BNB, MATIC, etc.)
        
        Args:
            w3: Web3 instance
            network_name: Network name
            
        Returns:
            Dictionary with balance info
        """
        try:
            network_config = NETWORKS[network_name]
            balance_wei = w3.eth.get_balance(self.wallet_address)
            balance = w3.from_wei(balance_wei, 'ether')
            
            native_token = network_config["native_token"]
            price = self.price_cache.get(native_token, 0)
            value_usd = float(balance) * price
            
            return {
                "symbol": native_token,
                "balance": float(balance),
                "value_usd": value_usd,
                "network": network_config["name"]
            }
            
        except Exception as e:
            logger.error(f"Error getting native balance on {network_name}: {str(e)}")
            return {"symbol": "", "balance": 0, "value_usd": 0, "network": ""}
    
    def _get_token_balance(self, w3: Web3, token_config: Dict, network_name: str) -> Optional[Dict]:
        """
        Get ERC-20 token balance
        
        Args:
            w3: Web3 instance
            token_config: Token configuration dictionary
            network_name: Network name
            
        Returns:
            Dictionary with balance info or None
        """
        try:
            token_address = Web3.to_checksum_address(token_config["address"])
            contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
            
            balance_raw = contract.functions.balanceOf(self.wallet_address).call()
            decimals = token_config["decimals"]
            balance = balance_raw / (10 ** decimals)
            
            # Skip if balance is zero
            if balance == 0:
                return None
            
            symbol = token_config["symbol"]
            price = self.price_cache.get(symbol, 0)
            value_usd = balance * price
            
            return {
                "symbol": symbol,
                "balance": balance,
                "value_usd": value_usd,
                "network": NETWORKS[network_name]["name"]
            }
            
        except Exception as e:
            # Silent fail for individual tokens (common for tokens user doesn't have)
            return None
    
    def check_network_balance(self, network_name: str) -> List[Dict]:
        """
        Check all balances on a specific network
        
        Args:
            network_name: Network name
            
        Returns:
            List of balance dictionaries
        """
        balances = []
        
        try:
            w3 = self._get_web3_connection(network_name)
            if not w3:
                return balances
            
            # Get native token balance
            native_balance = self._get_native_balance(w3, network_name)
            if native_balance["balance"] > 0:
                balances.append(native_balance)
            
            # Get ERC-20 token balances
            tokens = get_tokens_for_network(network_name)
            for token in tokens:
                token_balance = self._get_token_balance(w3, token, network_name)
                if token_balance:
                    balances.append(token_balance)
            
            if balances:
                logger.info(f"✓ {NETWORKS[network_name]['name']}: Found {len(balances)} asset(s)")
            
        except Exception as e:
            logger.error(f"Error checking {network_name} balance: {str(e)}")
        
        return balances
    
    def check_all_balances(self) -> Dict[str, any]:
        """
        Check balances across all supported networks
        
        Returns:
            Dictionary with all balances and total USD value
        """
        print("\n")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║           🔍 MULTI-CHAIN BALANCE SCANNER 🔍                     ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print(f"\n💼 Wallet Address: {self.wallet_address}")
        print(f"🌐 Scanning 5 blockchain networks...")
        print("\n" + "─" * 70)
        
        logger.info("Starting multi-chain balance check...")
        
        # Fetch prices first
        print("\n📊 Fetching token prices from CoinGecko...")
        self._fetch_token_prices()
        print(f"✓ Loaded prices for {len(self.price_cache)} tokens")
        
        all_balances = []
        network_summaries = {}
        
        # Check each network
        networks = get_all_networks()
        for idx, network_name in enumerate(networks, 1):
            print(f"\n[{idx}/{len(networks)}] Scanning {NETWORKS[network_name]['name']}...")
            network_balances = self.check_network_balance(network_name)
            all_balances.extend(network_balances)
            
            # Calculate network total
            network_total = sum(b["value_usd"] for b in network_balances)
            if network_total > 0:
                network_summaries[network_name] = {
                    "total_usd": network_total,
                    "asset_count": len(network_balances)
                }
                print(f"   ✓ Found {len(network_balances)} asset(s) worth ${network_total:.2f}")
            else:
                print(f"   ○ No assets found")
        
        # Calculate total
        total_value_usd = sum(b["value_usd"] for b in all_balances)
        
        result = {
            "wallet_address": self.wallet_address,
            "total_value_usd": total_value_usd,
            "total_assets": len(all_balances),
            "networks": network_summaries,
            "balances": all_balances
        }
        
        # Print detailed summary
        print("\n\n")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                  💰 PORTFOLIO SUMMARY 💰                         ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        
        if all_balances:
            print("\n" + "─" * 70)
            print(f"{'Asset':<12} {'Amount':>18} {'Value (USD)':>15} {'Network':<20}")
            print("─" * 70)
            
            for balance in sorted(all_balances, key=lambda x: x['value_usd'], reverse=True):
                print(f"{balance['symbol']:<12} {balance['balance']:>18.6f} "
                      f"${balance['value_usd']:>14.2f} {balance['network']:<20}")
            
            print("─" * 70)
            print(f"{'TOTAL VALUE':>30} ${total_value_usd:>14.2f}")
            print("─" * 70)
        else:
            print("\n⚠ No assets found across any network")
            print("Please ensure your wallet has funds on supported networks.")
        
        print("\n" + "═" * 70 + "\n")
        
        logger.info(f"Balance check completed: ${total_value_usd:.2f} total value")
        
        return result
